from django.test import TestCase
from users.models import UserRole
from bank.tests.factory_models.models import BankFactory, CompanyFactory
from users.tests.factory_models.models import CustomUserFactory


def make_login(self, username, password):
    return self.client.post('/api/login/', {'username': username, 'password': password})


def give_dt_banks(self):
    return {
        "name": "bank1", "code": "1234", "branch_code": "123",
        "address": "address1", "email": "bank1@mail.fr",
        "phone": "+331449055", "holder_name": "holder1",
        "country_key": "FR", "rib_key": "12", "swift": "BANK1FRXXX",
        "company": self.c1.id
    }, {
        "name": "bank2", "code": "5678", "branch_code": "567",
        "address": "address2", "email": "bank2@mail.fr",
        "phone": "+331449055", "holder_name": "holder2",
        "country_key": "FR", "rib_key": "23", "swift": "BANK2FRXXX",
        "company": self.c2.id
    }


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

        self.ad1.set_password("adm123")
        self.ad2.set_password("adm123")
        self.ad1.save()
        self.ad2.save()

        self.c1.users.add(self.ad1)
        self.c2.users.add(self.ad2)
        self.c1.save()
        self.c2.save()

    def test_company_creation(self):
        assert self.ad1 in self.c1.users.all()
        assert self.ad2 in self.c2.users.all()

    def test_bank_creat1(self):
        make_login(self, "admin1", "adm123")
        d1, d2 = give_dt_banks(self)
        r1 = self.client.post("/api/banks/", d1,
                              content_type='application/json')
        r2 = self.client.post("/api/banks/", d2,
                              content_type='application/json')

        assert r1.status_code == 201
        assert r2.status_code == 403

    def test_bank_creat2(self):
        make_login(self, "admin2", "adm123")
        d1, d2 = give_dt_banks(self)
        r1 = self.client.post("/api/banks/", d1,
                              content_type='application/json')
        r2 = self.client.post("/api/banks/", d2,
                              content_type='application/json')

        assert r1.status_code == 403
        assert r2.status_code == 201


    def test_bank_update(self):
        ...

    def test_bank_delete(self):
        ...