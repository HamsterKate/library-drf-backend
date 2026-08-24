from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer


class BorrowingViewSet(ReadOnlyModelViewSet):
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Borrowing.objects.select_related("book", "user")

        if self.request.user.is_staff:
            user_id = self.request.query_params.get("user_id")

            if user_id:
                queryset = queryset.filter(user_id=user_id)

            return queryset

        return queryset.filter(user=self.request.user)