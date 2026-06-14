from django.urls import path, include
from . import views
from bank.views import BankFileViewset, BankViewset, AccountViewset, \
    OperationViewset, CompanyViewset
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

router = routers.DefaultRouter()
router.register(r'bankfiles', BankFileViewset, basename='bankfiles')
router.register(r'companies', CompanyViewset, basename='companies')
router.register(r'banks', BankViewset, basename='banks')

# Nested routes for accounts adn operations
bank_router = NestedSimpleRouter(router, r'banks', lookup='bank')
bank_router.register(r'accounts', AccountViewset, basename='accounts')
oper_router = NestedSimpleRouter(bank_router, r'accounts', lookup='account')
oper_router.register(r'operations', OperationViewset, basename='operation')

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
    path('api/', include(bank_router.urls)),
    path('api/', include(oper_router.urls)),

    path('welcome/', views.welcome, name='welcome'),
    path('list_banks/', views.bank, name='bank'),
    path('check_file/', views.check_file, name='check_file'),
    path('charge_data/', views.charge_data, name='charge_data'),
    path('update_bank_form/<uuid:bank_id>/', views.update_bank_form, name='update_bank_form'),
    path('bank_preview/', views.bank_details, name='bank_preview'),
    path('chargefile/', views.charge_file, name='charge_file'),
    path('importdocuments/', views.importdocument, name='import'),
    path('statements/', views.accounts_statement, name='statements'),
    path('archived/', views.archived_files, name='archived_files'),
]
