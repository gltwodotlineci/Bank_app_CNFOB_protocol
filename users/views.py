from django.http import HttpResponse
from django.shortcuts import redirect, render
from rest_framework import renderers, viewsets
from bank.models import Bank
from users.models import CustomUser
from rest_framework.views import APIView, Response
from django.contrib.auth import authenticate, login, logout

from users.serializers import UserSerializer, LoginSerializer


def authent_usr(request):
    return render(request, 'users/login.html', {})

def signup(request):
    return render(request, 'users/signup.html', {})

def new_user(request):
    return render(request, 'users/new_user.html', {})


class RegisterUserView(APIView):
    """
    Create new user
    Methods: post
    """
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.create_user(
                username=data.get('username'),
                email=data.get('email'),
                password=data.get('password')
            )
            user.save()
            login(request, user)

            response = HttpResponse()
            response["HX-Redirect"] = "/new_user/"
            return response

        msg = "The username or the email already exists"
        return Response({'message': f'Error creating user {msg}'})


class LoginUserView(APIView):
    """
    Login user:
    Methods: post
    """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            serializer_valid = serializer.validated_data
            username = serializer_valid.get('username')
            password = serializer_valid.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)

                response = HttpResponse()
                response["HX-Redirect"] = "/welcome/"
                return response

            return Response({'message': 'Invalid username or password'})


class LogoutUserView(APIView):
    """
    Log out user:
    Methods: post
    """
    def post(self, request):
        logout(request)

        response = HttpResponse()
        response["HX-Redirect"] = "/"
        return response


class UserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    lookup_field = 'pk'
    http_method_names = ['get', 'patch', 'delete', 'put']


def admin_page(request):
    user = request.user
    if user.is_superuser or user.role == "A":
        users = CustomUser.objects.all()
        users = users.exclude(username=user.username)
        banks = Bank.objects.all()
        return render(request, 'users/admin_page.html',
                      {"users": users, "banks": banks})
    else:
        return redirect('home')


def user_modal(request):
    return render(request, 'users/partials/user_modal.html')
