from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import UserRole


class CompanyPermission(BasePermission):
    """
    Custom permission to only allow users of a company to access its data.
    """
    def has_permission(self, request, view) -> bool:
        if not request.user.is_authenticated:
            return False
        if request.method == "POST":
            if request.user.is_superuser:
                return True
            return request.user.role == UserRole.ADMIN
        return True

    def has_object_permission(self, request, view, obj):
        # Check if the user is associated with the company
        user = request.user
        if user.is_superuser:
            return True

        if request.method in SAFE_METHODS:
            return obj.users.filter(id=user.id).exists()

        if request.method in ["DELETE", "PATCH", "POST"]:
            return obj.users.filter(id=user.id).exists()


class BankAccountPermission(BasePermission):
    """
    Custom permission to only allow users of a bank to access its data.
    """
    def has_permission(self, request, view) -> bool:
        user = request.user
        if not user.is_authenticated:
            return False
        if request.method == "POST":
            return user.role in [UserRole.ADMIN, UserRole.MANAGER, UserRole.STAFF]
        return True

    def has_object_permission(self, request, view, obj):
        # Check if the user is associated with the bank
        user = request.user
        if user.is_superuser:
            return True

        if request.method in SAFE_METHODS:
            return user.role in [UserRole.ADMIN, UserRole.STAFF, UserRole.MANAGER]

        if request.method in ["DELETE", "PATCH"]:
            return user.role in [UserRole.ADMIN, UserRole.MANAGER]

        return False


class FileOperationPermission(BasePermission):
    """
    Custom permission to only allow users of a bank to access its data.
    """
    def has_permission(self, request, view) -> bool:
        user = request.user
        if not user.is_authenticated:
            return False
        if request.method == "POST":
            return user.role in [UserRole.ADMIN, UserRole.STAFF]
        return True

    def has_object_permission(self, request, view, obj):
        # Check if the user is associated with the bank
        user = request.user
        if user.is_superuser:
            return True

        if request.method in SAFE_METHODS:
            return user.role in [UserRole.ADMIN, UserRole.STAFF, UserRole.MANAGER]

        if request.method in ["DELETE", "PATCH"]:
            return user.role in [UserRole.ADMIN, UserRole.MANAGER]
