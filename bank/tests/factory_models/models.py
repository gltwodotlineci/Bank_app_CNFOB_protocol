import factory
from bank.models import Company


class CompanyFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating CustomUser instances for testing.
    """
    class Meta:
        model = Company

    name = factory.Faker('name')
    company_code = factory.Faker('text', max_nb_chars=19)
    company_address = factory.Faker('address')
    company_email = factory.Faker('email')
    company_phone = factory.Faker('phone_number')
    company_website = factory.Faker('url')
    company_logo = factory.django.ImageField(color='blue')

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for user in extracted:
                self.users.add(user)
