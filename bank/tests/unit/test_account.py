from django.test import TestCase
from bank.tests.factory_models.models import Account, Bank, CompanyBank, Company
from users.models import UserRole
from users.tests.factory_models.models import CustomUserFactory
from bank.tests.factory_models.models import CompanyFactory, BankFactory, CompanyBankFactory


def make_login(self, username, password):
    return self.client.post('/api/login/', {'username': username, 'password': password}, format='json')


def give_dt_banks():
    return {"name": "bank3", "code": "9012", "branch_code": "901",
        "adresse": "address3", "email": "bank3@mail.fr",
        "phone": "+331449055", "holder_name": "holder3",
        "country_key": "FR", "rib_key": "34",
        "swift": "BANK3FRXX"}, {"name": "bank4", "code": "3456",
        "branch_code": "345", "adresse": "address4", "email": "bank4@mail.fr",
        "phone": "+331449055", "holder_name": "holder4", "country_key": "FR",
        "rib_key": "45", "swift": "BANK4FRXXX"}


class AccountTestCase(TestCase):
    def setUp(self):
        self.ad1 = CustomUserFactory.create(
            username='ad1', role=UserRole.ADMIN,
            email='ad1@example.com')
        self.ad2 = CustomUserFactory.create(
            username='ad2', role=UserRole.ADMIN,
            email='ad2@example.com')
        self.ad1.set_password('1234')
        self.ad2.set_password('1234')

        self.c1 = CompanyFactory.create(name="comp1",
                                        company_code="1234567890",
                                        company_email="comp1@mail.fr",
                                        company_phone="+331339087")

        self.c2 = CompanyFactory.create(name="comp2",
                                        company_code="0987654321",
                                        company_email="comp2@mail.fr",
                                        company_phone="+331449055")
        self.c1.users.add(self.ad1.save())
        self.c2.users.add(self.ad2.save())
        d1, d2 = give_dt_banks()
        self.b1 = BankFactory.create(**d1)
        self.b2 = BankFactory.create(**d2)
        CompanyBankFactory(company=self.c1, bank=self.b1,
                           swift=self.b1.swift)
        CompanyBankFactory(company=self.c2, bank=self.b2,
                           swift=self.b2.swift)

    def test_account_creation(self):
        case=[
            ('ad1', '9154678901',  str(self.b1.id)),
            ('ad2', '9516487902',  str(self.b1.id)),
        ]
        for dt in case:
            usr, num, url = dt

            make_login(self, usr, '1234')
            res = self.client.post(f'/api/banks/{url}/accounts/',
                                {'number': num,
                                    'bank': self.b1.id,
                                    'amount': 10000.00},
                                    content_type='application/json')

            assert res.status_code == 201
