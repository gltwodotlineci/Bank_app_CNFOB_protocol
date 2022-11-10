from django.contrib import admin
from .models import Bank, AccountNumber, SelectDocument, ImportingDocument
from .models import AccountNumber

admin.site.register(Bank)
admin.site.register(AccountNumber)
admin.site.register(SelectDocument)
admin.site.register(ImportingDocument)
# Register your models here.
