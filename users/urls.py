from django.urls import path
from users.views import RegisterUserView, LoginUserView, LogoutUserView
from users.views import authent_usr, signup, new_user
from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
    path('auth/', authent_usr, name='login'),
    path('signup/', signup, name='signup'),
    path('new_user/', new_user, name='new_user'),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/login/', LoginUserView.as_view(), name='login'),
    path('api/logout/', LogoutUserView.as_view(), name='logout'),
]


