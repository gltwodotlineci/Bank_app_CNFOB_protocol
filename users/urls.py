from django.urls import path, include
from users.views import RegisterUserView, LoginUserView, LogoutUserView, UserViewset
from users.views import authent_usr, signup, new_user, admin_page, user_modal
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewset)


urlpatterns = [
    path('api/', include(router.urls)),
    path('auth/', authent_usr, name='login'),
    path('signup/', signup, name='signup'),
    path('new_user/', new_user, name='new_user'),
    path('admin_page/', admin_page, name='admin-page'),
    path('user_modal/', user_modal, name='user-modal'),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/login/', LoginUserView.as_view(), name='login'),
    path('api/logout/', LogoutUserView.as_view(), name='logout'),
]


