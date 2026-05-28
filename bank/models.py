from datetime import datetime

from django.db import models
from uuid import uuid4
from bank_CFNOB_norm import settings
from users.models import CustomUser


class Company(models.Model):
    """
    Company Model for the
    Attributes:
        id: Unique id for the company
        name: Name of the company
        company_code: Company code
        company_address: Address of the company
        company_email: Email of the company
        company_phone: Phone number of the company
        company_website: Website of the company
        company_logo: Logo of the company
        company_bank: Bank of the company
        company_account: Account of the company
        company_account_number: Account number of the company
        company_account_currency: Currency of the company account
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    users = models.ManyToManyField(CustomUser, related_name='companies')
    name = models.CharField(max_length=100)
    company_code = models.CharField(max_length=100)
    company_address = models.CharField(max_length=100)
    company_email = models.EmailField()
    company_phone = models.CharField(max_length=100)
    company_website = models.CharField(max_length=100)
    company_logo = models.ImageField(upload_to='company_logos/')


class Bank(models.Model):
    """
    Bank Model for the
    Attributes:
        id: Unique id for the bank
        name_bank: Name of the bank
        bank_code: Bank code
        branch_code: Branch code
        bic: BIC code
        bank_address: Address of the bank
        country_key: Country key
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL,
                             null=True,
                             related_name='bank')
    name = models.CharField(max_length=60, unique=True)
    code = models.CharField(max_length=5, unique=True)
    branch_code = models.CharField(max_length=5)
    rib_key = models.CharField(max_length=2)
    swift = models.CharField(max_length=12, verbose_name='SWIFT')
    holder_name = models.CharField(max_length=80)
    adresse = models.CharField(max_length=80, null=True, blank=True)
    zip_code = models.CharField(max_length=5, null=True, blank=True)
    country_key = models.CharField(max_length=4)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Currency(models.TextChoices):
    EUR = 'E'
    USR = 'U'
    CNY = 'C'


class Account(models.Model):
    """
    Account Number Model for the
    Attributes:
        id: Unique id for the account number
        account_number: Account number
        rib_key: RIB key
        bank: Bank as FK
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    number = models.CharField(max_length=15)
    bank = models.ForeignKey(Bank, on_delete=models.SET_NULL,
                             related_name='accounts', null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=1, choices=Currency.choices,
                                default=Currency.EUR)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.number


class BankStatementFile(models.Model):
    """
    Imported file model for the bank data
    Attributes:
        id: Unique id for the imported file
        name: Name of the imported file
        archived: State of the imported file
        date_imported: Date of the imported file
        date_generated: Date of the generated file
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)    
    name = models.FileField(upload_to='bank_statements/')
    archived = models.BooleanField(default=False)
    date_imported = models.DateField(auto_now_add=True)
    checked = models.BooleanField(default=False)
    date_generated = models.DateField(null=True, blank=True)
    date_updated = models.DateField(auto_now=True)
    bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True)


class Operation(models.Model):
    """
    Operation Model for the bank data
    Attributes:
        id (integer): Unique id for the operation
        record_code (str): Record code
        bank_code (str): Bank code
        account_number (str): Account number
        date (date): Operation date
        label (str): Operation label
        amount (decimal): Amount credited or debited
        credit_debit (str): Credit or Debit
    """
    id = models.AutoField(primary_key=True, editable=False)
    record_code = models.CharField(max_length=3)
    bank_code = models.CharField(max_length=7)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    label = models.CharField(max_length=45, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    CREDIT, DEBIT, LABEL = 'C', 'D', 'N'
    CREDIT_DEBIT = [(CREDIT, 'Credit'),
                    (DEBIT, 'Debit'),
                    (LABEL, 'Label')]
    credit_or_debit = models.CharField(max_length=1, choices=CREDIT_DEBIT)
    pointed = models.BooleanField(default=False)
    pointer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                null=True, blank=True)
    date_pointed = models.DateTimeField(null=True, blank=True)


class NewBalanceAccount(models.Model):
    """
    New Balance Account Model for the bank data
    Attributes:
        id: Unique id for the new balance account
        enrolling_nb: Enrolling number
        bank_code: Bank code
        account_number: Account number
        new_balance_date: New balance date
        new_balance: New balance
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    enrolling_nb = models.CharField(max_length=3)
    bank_code = models.CharField(max_length=7)
    account_number = models.CharField(max_length=15)
    new_balance_date = models.DateTimeField()
    amount_credit = models.DecimalField(max_digits=12, decimal_places=2)
    amount_debit = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.enrolling_nb
