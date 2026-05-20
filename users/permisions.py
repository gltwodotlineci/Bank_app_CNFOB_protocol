from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import CustomUser, UserRole


class IsManager(BasePermission):
    """
    Allows access only to manager users.
    """
    def has_permission(self, request, view) -> bool:
        return True

    # def has_object_permission(self, request, view, obj):
    #     if request.user.is_superuser:
    #         return True

    #     if request.method in SAFE_METHODS:
    #         user = request.user
    #         if user.is_superuser:
    #             return True
    #         return user.role == UserRole.MANAGER

    #     if request.method in ["DELETE", "PATCH", "PUT"]:
    #         user = request.user
    #         if user.is_superuser:
    #             return True
    #         return user.role == UserRole.MANAGER

    #     return False
