import factory
import Decimal
from bank.models import Company, Bank, CompanyBank, Account
from users.tests.factory_models.models import CustomUserFactory


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

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for user in extracted:
                self.users.add(user)


class BankFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating CustomUser instances for testing.
    """
    class Meta:
        model = Bank

    name = factory.Faker('name')
    user = factory.SubFactory(CustomUserFactory)
    code = factory.Faker('text', max_nb_chars=8)
    branch_code = factory.Faker('text', max_nb_chars=6)
    rib_key = factory.Faker('text', max_nb_chars=2)
    swift = factory.Faker('text', max_nb_chars=19)
    adresse = factory.Faker('address')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    holder_name = factory.Faker('name')
    country_key = factory.Faker('text', max_nb_chars=4)


class CompanyBankFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating CompanyBank instances for testing.
    """
    class Meta:
        model = CompanyBank

    company = factory.SubFactory(CompanyFactory)
    bank = factory.SubFactory(BankFactory)
    swift = factory.Faker('text', max_nb_chars=24)

class AccountFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Account instances for testing.
    """
    class Meta:
        model = Account

    number = factory.Faker('text', max_nb_chars=24)
    bank = factory.SubFactory(BankFactory)
    amount = factory.Faker('text', max_nb_chars=24)
    currency = Decimal("100.50")
    active = True
