from django.contrib import admin
from .models import Bank, AccountNumber, SelectDocument, ImportingDocument,\
    AccountNumber, FileUpload

admin.site.register(Bank)
admin.site.register(AccountNumber)
admin.site.register(SelectDocument)
admin.site.register(ImportingDocument)
admin.site.register(FileUpload)
# Register your models here.
