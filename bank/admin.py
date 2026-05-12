from django.contrib import admin
from .models import Bank, AccountNumber, BankStatementFile,\
    Operation, NewBalanceAccount

admin.site.register(Bank)
admin.site.register(AccountNumber)
admin.site.register(BankStatementFile)
admin.site.register(Operation)
admin.site.register(NewBalanceAccount)
# Register your models here.
