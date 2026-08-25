from datetime import date

from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import (
    OpenApiParameter, OpenApiTypes, extend_schema, extend_schema_view
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer, BorrowingCreateSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List borrowings",
        description=(
            "Retrieve borrowings for the authenticated user. "
            "Staff users can retrieve all borrowings and filter them "
            "by user ID. Borrowings can also be filtered by active status."
        ),
        parameters=[
            OpenApiParameter(
                name="user_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter borrowings by user ID. Available to staff users.",
                required=False,
            ),
            OpenApiParameter(
                name="is_active",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description=(
                    "Filter borrowings by active status. "
                    "Use true for active borrowings and false for returned borrowings."
                ),
                required=False,
            ),
        ],
    ),
    retrieve=extend_schema(
        summary="Retrieve a borrowing",
        description=(
            "Retrieve details of a borrowing. Regular users can access "
            "only their own borrowings. Staff users can access any borrowing."
        ),
    ),
    create=extend_schema(
        summary="Create a borrowing",
        description=(
            "Create a borrowing for the authenticated user. "
            "The book must have available inventory. "
            "The user and borrow date are set automatically."
        ),
        request=BorrowingCreateSerializer,
        responses={201: BorrowingCreateSerializer},
    ),
)
class BorrowingViewSet(ModelViewSet):
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer

        return BorrowingSerializer

    def get_queryset(self):
        queryset = Borrowing.objects.select_related("book", "user")

        if self.request.user.is_staff:
            user_id = self.request.query_params.get("user_id")

            if user_id:
                queryset = queryset.filter(user_id=user_id)
        else:
            queryset = queryset.filter(user=self.request.user)

        is_active = self.request.query_params.get("is_active")

        if is_active == "true":
            queryset = queryset.filter(actual_return_date__isnull=True)
        elif is_active == "false":
            queryset = queryset.filter(actual_return_date__isnull=False)

        return queryset

    @action(
        detail=True,
        methods=["post"],
        url_path="return",
    )
    @transaction.atomic
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date is not None:
            return Response(
                {"detail": "This borrowing has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        borrowing.actual_return_date = date.today()
        borrowing.save(update_fields=["actual_return_date"])

        borrowing.book.inventory += 1
        borrowing.book.save(update_fields=["inventory"])

        serializer = self.get_serializer(borrowing)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
