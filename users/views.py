from rest_framework import viewsets
from rest_framework.permissions import (
    AllowAny,
    BasePermission,
    IsAdminUser,
)
from drf_spectacular.utils import extend_schema, extend_schema_view

from users.models import User
from users.permissions import IsAdminOrSelf
from users.serializers import UserSerializer

@extend_schema_view(
    list=extend_schema(
        summary="List users",
        description="Retrieve a list of all users. Available to administrators only.",
    ),
    create=extend_schema(
        summary="Create a user",
        description="Create a new customer account.",
    ),
    retrieve=extend_schema(
        summary="Retrieve a user",
        description="Retrieve details of a user. Users can retrieve only their own profile, administrators can retrieve any user.",
    ),
    update=extend_schema(
        summary="Update a user",
        description="Update a user profile. Users can update only their own profile, administrators can update any user.",
    ),
    partial_update=extend_schema(
        summary="Partially update a user",
        description="Partially update a user profile. Users can update only their own profile, administrators can update any user.",
    ),
    destroy=extend_schema(
        summary="Delete a user",
        description="Delete a user. Available to administrators only.",
    ),
)
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
