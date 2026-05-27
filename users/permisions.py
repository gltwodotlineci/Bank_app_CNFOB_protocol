from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import CustomUser, UserRole


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
            if user in obj.get(user=user):
                return True
            return user.role == UserRole.MANAGER

        if request.method in ["DELETE", "PATCH", "PUT"]:
            return user.role == UserRole.MANAGER

        return False
