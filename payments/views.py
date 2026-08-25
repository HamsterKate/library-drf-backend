from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from payments.models import Payment
from payments.serializers import PaymentSerializer


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
