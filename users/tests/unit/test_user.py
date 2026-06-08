from django.test import TestCase
from rest_framework.test import APIClient
from users.models import User, UserRole
from users.tests.factory_models.models import CustomUserFactory


class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUserFactory.create()

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)

    def test_user_role(self):
        self.assertEqual(self.user.role, UserRole.USER)

    def test_user_password(self):
        self.assertTrue(self.user.check_password('password'))
