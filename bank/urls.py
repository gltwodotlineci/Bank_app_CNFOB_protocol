from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list_banks/', views.bank, name='bank'),
    path('importdata/', views.importdata, name='import'),
    path('statement_of_acounts/', views.statement_of_accounts, name='statement of accounts'),
    path('general_view/', views.general_view, name="general view"),
]