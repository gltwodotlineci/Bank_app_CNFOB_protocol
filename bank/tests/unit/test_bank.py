from django.test import TestCase
from users.models import UserRole
from bank.tests.factory_models.models import BankFactory, CompanyFactory, \
    CompanyBankFactory
from users.tests.factory_models.models import CustomUserFactory


def make_login(self, username, password):
    return self.client.post('/api/login/', {'username': username, 'password': password})


def give_dt_banks(self):
    return {
        "name": "bank1", "code": "1234", "branch_code": "123",
        "adresse": "address1", "email": "bank1@mail.fr",
        "phone": "+331449055", "holder_name": "holder1",
        "country_key": "FR", "rib_key": "12", "swift": "BANK1FRXXX",
        "company": self.c1.id
    }, {
        "name": "bank2", "code": "5678", "branch_code": "567",
        "adresse": "address2", "email": "bank2@mail.fr",
        "phone": "+331449055", "holder_name": "holder2",
        "country_key": "FR", "rib_key": "23", "swift": "BANK2FRXXX",
        "company": self.c2.id
    }, {"name": "bank3", "code": "9012", "branch_code": "901",
        "adresse": "address3", "email": "bank3@mail.fr",
        "phone": "+331449055", "holder_name": "holder3",
        "country_key": "FR", "rib_key": "34",
        "swift": "BANK3FRXX"}, {"name": "bank4", "code": "3456",
        "branch_code": "345", "adresse": "address4", "email": "bank4@mail.fr",
        "phone": "+331449055", "holder_name": "holder4", "country_key": "FR",
        "rib_key": "45", "swift": "BANK4FRXXX"}


class BankTestCase(TestCase):
    def setUp(self):
        self.c1 = CompanyFactory.create(name="comp1",
                                        company_code="1234567890",
                                        company_email="comp1@mail.fr",
                                        company_phone="+331339087")

        self.c2 = CompanyFactory.create(name="comp2",
                                        company_code="0987654321",
                                        company_email="comp2@mail.fr",
                                        company_phone="+331449055")

        self.ad1 = CustomUserFactory.create(username="admin1",
                                            email="ad1@mail.fr",
                                            role=UserRole.ADMIN)
        self.ad2 = CustomUserFactory.create(username="admin2",
                                            email="ad2@mail.fr",
                                            role=UserRole.ADMIN)

        # users password:
        self.ad1.set_password("adm123")
        self.ad2.set_password("adm123")
        self.ad1.save()
        self.ad2.save()

        # create companies
        self.c1.users.add(self.ad1)
        self.c2.users.add(self.ad2)
        self.c1.save()
        self.c2.save()

        # create banks
        _, _, d3, d4 = give_dt_banks(self)
        d3["user"] = self.ad1
        self.bank1 = BankFactory.create(**d3)
        self.bank2 = BankFactory.create(**d4)

        CompanyBankFactory(company=self.c1, bank=self.bank1,
                           swift=self.bank1.swift)
        CompanyBankFactory(company=self.c2, bank=self.bank2,
                           swift=self.bank2.swift)

    def test_company_creation(self):
        assert self.ad1 in self.c1.users.all()
        assert self.ad2 in self.c2.users.all()

    def test_bank_creat1(self):
        make_login(self, "admin1", "adm123")
        d1, d2, _, _ = give_dt_banks(self)
        r1 = self.client.post("/api/banks/", d1,
                              content_type='application/json')
        r2 = self.client.post("/api/banks/", d2,
                              content_type='application/json')
        assert r1.status_code == 201
        assert r2.status_code == 403

    def test_bank_creat2(self):
        make_login(self, "admin2", "adm123")
        d1, d2, _ , _ = give_dt_banks(self)
        r1 = self.client.post("/api/banks/", d1,
                              content_type='application/json')
        r2 = self.client.post("/api/banks/", d2,
                              content_type='application/json')

        assert r1.status_code == 403
        assert r2.status_code == 201

    def test_bank_update(self):
        case = [
            ("admin1", "adm123", "m1@mail.com", str(self.bank1.id), 200),
            ("admin2", "adm123", "m2@mail.com", str(self.bank1.id), 404),
            ("admin1", "adm123", "m1@mail.com", str(self.bank2.id), 404),
            ("admin2", "adm123", "m2@mail.com", str(self.bank2.id), 200),            
        ]
        for dt in case:
            usr, pwd, email, url, status = dt

            make_login(self, usr, pwd)
            res = self.client.patch(f'/api/banks/{url}/',
                                {"holder_name": "new_name",
                                "email": email},
                                content_type='application/json')
            assert res.status_code == status
