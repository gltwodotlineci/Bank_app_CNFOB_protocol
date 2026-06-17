from django.test import TestCase
from users.models import UserRole
from users.tests.factory_models.models import CustomUserFactory
from bank.tests.factory_models.models import CompanyFactory


def make_login(self, username, password):
    return self.client.post('/api/login/', {'username': username, 'password': password})


class UserTestCase(TestCase):
    def setUp(self):
        self.user_admin = CustomUserFactory.create(
            role=UserRole.ADMIN,
            username='admin_user',
            email='admin@gmail.com'
        )
        self.user_admin.set_password('admin1234')
        self.user_admin.save()
        self.user = CustomUserFactory.create(
            role=UserRole.VISITOR,
            username='user',
            email='user@gmail.com'
        )
        self.user.set_password('user1234')
        self.user.save()        
        self.company = CompanyFactory.create()

    def test_login(self):
        make_login(self, "user", "user1234")
        response = self.client.post('/api/login/',
                                    data={'username': 'user', 'password': 'user1234'},
                                    content_type='application/json')
        assert response.status_code == 200

    def test_logout(self):
        make_login(self, "user", "user1234")
        response = self.client.post('/api/logout/',
                                    content_type='application/json')
        assert response.status_code == 200

    def test_user_update(self):
        make_login(self, "admin_user", "admin1234")
        self.client.patch(f'/api/users/{self.user.id}/',
                      data={'role': UserRole.MANAGER},
                      content_type='application/json')

        self.user.refresh_from_db()
        assert self.user.role == UserRole.MANAGER

    def test_no_auth(self):
        make_login(self, "user", "user1234")
        ad_us = self.user_admin
        self.client.patch(f'/api/users/{ad_us.id}/',
                      data={'role': UserRole.MANAGER},
                      content_type='application/json')
        self.user.refresh_from_db()
        assert self.user_admin.role == UserRole.ADMIN

