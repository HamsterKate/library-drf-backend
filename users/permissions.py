from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from users.models import User


class IsAdminOrSelf(permissions.BasePermission):
    """Allow admins or the user to access the object."""

    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj: User,
    ) -> bool:
        return (
            request.user.is_authenticated
            and (request.user.is_staff or obj == request.user)
        )