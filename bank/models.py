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

    def __str__(self):
        return self.account_number
    #branch_code = Bank.objects.get(id=bank)
    #iban = branch_code.branch_code + account_number


class ImportingDocument(models.Model):
    name_document = models.CharField(max_length=15)
    date_imported = models.CharField(max_length=10)

    def __str__(self):
        return self.name_document

class FileUpload(models.Model):
    file = models.FileField()
    created_at = models.DateField()


class OldAccount(models.Model):
    enrolling_nb = models.CharField(max_length=3)
    bank_code = models.CharField(max_length=7)
    account_number = models.CharField(max_length=15)
    date = models.CharField(max_length=10)
    amount_credit = models.CharField(max_length=15)
    amount_debit = models.CharField(max_length=15)

    def __str__(self):
        return self.enrolling_nb


class Operation(models.Model):
    enrolling_nb = models.CharField(max_length=3)
    bank_code = models.CharField(max_length=7)
    account_number = models.CharField(max_length=15)
    operation_date = models.CharField(max_length=10)
    operation_name = models.CharField(max_length=10)
    amount_credit = models.CharField(max_length=15)
    amount_debit = models.CharField(max_length=15)

    def __str__(self):
        return self.enrolling_nb


class NewBalanceAccount(models.Model):
    enrolling_nb = models.CharField(max_length=3)
    bank_code = models.CharField(max_length=7)
    account_number = models.CharField(max_length=15)
    new_balance_date = models.CharField(max_length=10)
    amount_credit = models.CharField(max_length=15)
    amount_debit = models.CharField(max_length=15)

    def __str__(self):
        return self.enrolling_nb



