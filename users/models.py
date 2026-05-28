
from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4


class UserRole(models.TextChoices):
    MANAGER = 'M', 'Manager'
    ADMIN = 'A', 'Admin'
    STAFF = 'S', 'Staff'
    REGULAR = 'R', 'Regular',
    VISITOR = 'V', 'Visitor'


class CustomUser(AbstractUser):
    """
    Creating Custom User Model
    Attributes:
        id: Unique id for the user
        role: Role of the user
        email: Email of the user
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    role = models.CharField(max_length=1, choices=UserRole.choices, default=UserRole.VISITOR)
    email = models.EmailField(unique=True)
