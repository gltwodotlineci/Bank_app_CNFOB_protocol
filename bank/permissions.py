from rest_framework.permissions import BasePermission, SAFE_METHODS
from bank.models import Company


class CompanyPermission(BasePermission):
    """
    Custom permission to only allow users of a company to access its data.
    """
    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if the user is associated with the company
        user = request.user
        if user.is_superuser:
            return True

        if request.method in SAFE_METHODS:
            return obj.users.filter(id=user.id).exists()

        if request.method in ["DELETE", "PATCH", "POST"]:
            return obj.users.filter(id=user.id).exists()
