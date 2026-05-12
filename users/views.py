from django.shortcuts import render
from rest_framework import render
from users.models import CustomUser
from rest_framework.views import ApiView


class RegisterUserView(ApiView):
    """
    Create new user
    Methods: post
    """
    def post(self, request):
        pass


class LoginUserView(ApiView):
    """
    Login user:
    Methods: post
    """
    def post(self, request):
        pass


class LogoutUserView(ApiView):
    """
    Log out user:
    Methods: post
    """
    def post(self, request):
        pass
