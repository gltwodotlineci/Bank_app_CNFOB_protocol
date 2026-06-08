import factory
from users.models import CustomUser, UserRole
from user_authent.tests.factory_models.models import UserFactory


class CustomUserFactory(UserFactory):
    """
    Factory for creating CustomUser instances for testing.
    """
    class Meta:
        model = CustomUser

    role = UserRole.STAFF
    username = factory.Faker('name')
    email = factory.Faker('email')
    active = True
