from django.http import HttpResponse
from django.shortcuts import redirect, render
from rest_framework import renderers, viewsets
from bank.models import Bank
from users.models import CustomUser
from rest_framework.views import APIView, Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from users.permisions import IsAdmin
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

            return Response({'message': 'User created successfully',
                             "redirect_url": "/new_user/"})

        msg = "The username or the email already exists"
        return Response({'message': f'Error creating user {msg}'},
                        status=400)


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

                return Response({'message': 'Login successful',
                                "redirect_url": "/welcome/"})

            return Response({
                "message": "Invalid username or password"
            }, status=400)


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
    """
    User Viewset for the admin page
    Methods: get, patch, delete, put
    """
    permission_classes = [IsAuthenticated, IsAdmin]
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
