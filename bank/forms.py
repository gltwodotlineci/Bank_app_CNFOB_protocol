from django.forms import ModelForm
from django import forms
from .models import Bank
from .models import AccountNumber

# class BankForm(ModelForm):
#     class Meta:
#         model = Bank
#         fields = '__all__'

# class AccountForm(ModelForm):
#     class Meta:
#         model = AccountNumber
#         fields = ['account_number','bank']
        #fields = '__all__'


class UploadFile(forms.Form):
    pass #file = forms.FileField()

