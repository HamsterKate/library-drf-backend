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
            "by user ID."
        ),
        parameters=[
            OpenApiParameter(
                name="user_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter borrowings by user ID. Available to staff users.",
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

            return queryset

        return queryset.filter(user=self.request.user)
