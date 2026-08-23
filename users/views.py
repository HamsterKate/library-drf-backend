from rest_framework import viewsets
from rest_framework.permissions import (
    AllowAny,
    BasePermission,
    IsAdminUser,
)

from users.models import User
from users.permissions import IsAdminOrSelf
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self) -> list[BasePermission]:
        if self.action == "create":
            permission_classes = [AllowAny]
        elif self.action in ("list", "destroy"):
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAdminOrSelf]

        return [permission() for permission in permission_classes]
