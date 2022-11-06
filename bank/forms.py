from django.forms import ModelForm
from .models import Bank

class BankForm(ModelForm):
    class Meta:
        model = Bank
        fields = '__all__'
