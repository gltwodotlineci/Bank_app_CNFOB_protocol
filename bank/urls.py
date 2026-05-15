from django.urls import path, include
from . import views
from bank.views import BankFileViewset, BankViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'bankfiles', BankFileViewset)
router.register(r'banks', BankViewset)

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
    path('welcome/', views.welcome, name='welcome'),
    path('list_banks/', views.bank, name='bank'),
    path('bank_form', views.bank_form, name='bank_form'),
    path('account_form', views.account_form, name='account_form'),
    path('chargefile/', views.charge_file, name='charge_file'),
    path('importdocuments/', views.importdocument, name='import'),
    path('statement_of_accounts/', views.statement_of_accounts, name='statement of accounts'),
    path('general_view/', views.general_view, name="general view"),
    path('add_bank', views.createBank, name="new_bank"),
    path('add_account_number', views.createAccount, name="new_account_number")
]
