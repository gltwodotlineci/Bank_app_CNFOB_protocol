import factory
from users.models import CustomUser, UserRole


class CustomUserFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating CustomUser instances for testing.
    """
    class Meta:
        model = CustomUser

    role = UserRole.STAFF
    username = factory.Faker('name')
    email = factory.Faker('email')
    password = factory.Faker('text')
