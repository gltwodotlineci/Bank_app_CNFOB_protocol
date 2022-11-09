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
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    #branch_code = Bank.objects.get(id=bank)
    #iban = branch_code.branch_code + account_number

    def __str__(self):
        return self.account_number


'''
    @property
    def iban(self):
        iban_number = self.bank.country_bank_code + self.bank.country_key + self.bank.bank_code + \
               self.bank.branch_code + self.account_number + self.rib_key
        return iban_number
'''
