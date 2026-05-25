from django.contrib import admin
from .models import Bank, Account, BankStatementFile,\
    Operation, NewBalanceAccount, Company

class AccountAdmin(admin.ModelAdmin):
    list_display = ('number', 'bank', "id")

admin.site.register(Account, AccountAdmin)

admin.site.register(Company)
admin.site.register(Bank)
admin.site.register(BankStatementFile)
admin.site.register(Operation)
admin.site.register(NewBalanceAccount)
# Register your models here.
