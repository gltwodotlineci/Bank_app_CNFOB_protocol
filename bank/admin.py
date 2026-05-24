from django.contrib import admin
from .models import Bank, Account, BankStatementFile,\
    Operation, NewBalanceAccount, Company

admin.site.register(Company)
admin.site.register(Bank)
admin.site.register(Account)
admin.site.register(BankStatementFile)
admin.site.register(Operation)
admin.site.register(NewBalanceAccount)
# Register your models here.
