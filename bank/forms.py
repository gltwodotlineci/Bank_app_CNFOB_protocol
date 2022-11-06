from django.forms import ModelForm
from .models import Bank
from .models import AccountNumber

class BankForm(ModelForm):
    class Meta:
        model = Bank
        fields = '__all__'

class AccountForm(ModelForm):
    class Meta:
        model = AccountNumber
        fields = '__all__'