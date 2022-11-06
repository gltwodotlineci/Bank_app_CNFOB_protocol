from django.db import models

class Bank(models.Model):
    name_bank = models.CharField(max_length=60)
    bank_code = models.CharField(max_length=20)
    branch_code = models.CharField(max_length=8)
    bic = models.CharField(max_length=12)
    bank_adresse = models.CharField(max_length=80, blank=True)
    country_bank_code = models.CharField(max_length=5)
    country_key = models.CharField(max_length=4)

    def __str__(self):
        return self.name_bank


class AccountNumber(models.Model):
    account_number = models.CharField(max_length=15)
    rib_key = models.CharField(max_length=10)
    iban = models.CharField(max_length=20)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)

    def __str__(self):
        return self.account_number
