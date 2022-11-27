from django.contrib import admin
from .models import Bank, AccountNumber, ImportingDocument, AccountNumber,\
    FileUpload, OldAccount, Operation, NewBalanceAccount

admin.site.register(Bank)
admin.site.register(AccountNumber)
admin.site.register(ImportingDocument)
admin.site.register(FileUpload)
admin.site.register(OldAccount)
admin.site.register(Operation)
admin.site.register(NewBalanceAccount)
# Register your models here.
