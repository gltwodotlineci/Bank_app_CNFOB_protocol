from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import UserRole


class IsAdmin(BasePermission):
    """
    Allows access only to manager users.
    """
    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser:
            return True

        if request.method in SAFE_METHODS:
            return user == obj or user.role == UserRole.ADMIN

        if request.method in ["DELETE", "PATCH", "PUT"]:
            return user.role == UserRole.ADMIN

        return False
