from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view

from payments.models import Payment
from payments.serializers import PaymentSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List payments",
        description=(
            "Retrieve payments for the authenticated user. "
            "Staff users can retrieve all payments."
        ),
    ),
    retrieve=extend_schema(
        summary="Retrieve a payment",
        description=(
            "Retrieve details of a payment. Regular users can access "
            "only their own payments. Staff users can access any payment."
        ),
    ),
)
class PaymentViewSet(ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = Payment.objects.select_related(
            "borrowing",
            "borrowing__user",
        )

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(
            borrowing__user=self.request.user
        )
