from django.contrib import admin
from .models import Bank, Account, BankStatementFile,\
    Operation, NewBalanceAccount, Company, CompanyBank

class AccountAdmin(admin.ModelAdmin):
    list_display = ('number', 'bank', "id")

admin.site.register(Account, AccountAdmin)


class CompanyBankAdmin(admin.ModelAdmin):
    list_display = ('company', 'bank', "id")

admin.site.register(CompanyBank, CompanyBankAdmin)

admin.site.register(Company)
admin.site.register(Bank)
admin.site.register(BankStatementFile)
class OperationAdmin(admin.ModelAdmin):
    list_display = ('account', 'label', 'amount', 'pointed')

admin.site.register(Operation, OperationAdmin)

admin.site.register(NewBalanceAccount)
# Register your models here.
