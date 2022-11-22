from django.contrib import admin
from .models import Bank, AccountNumber, ImportingDocument, AccountNumber,\
    FileUpload, OldAccount

admin.site.register(Bank)
admin.site.register(AccountNumber)
admin.site.register(ImportingDocument)
admin.site.register(FileUpload)
admin.site.register(OldAccount)
# Register your models here.
