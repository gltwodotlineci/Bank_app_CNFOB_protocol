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
    user = models.ManyToManyField(CustomUser, related_name='company')
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
    company = models.ForeignKey(Company,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='baks_company')
    name = models.CharField(max_length=60)
    code = models.CharField(max_length=20)
    branch_code = models.CharField(max_length=8)
    rib_key = models.CharField(max_length=4)
    bic = models.CharField(max_length=12)
    holder_name = models.CharField(max_length=80)
    adresse = models.CharField(max_length=80, blank=True)
    zip_code = models.CharField(max_length=5)
    country_key = models.CharField(max_length=4)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class AccountNumber(models.Model):
    """
    Account Number Model for the
    Attributes:
        id: Unique id for the account number
        account_number: Account number
        rib_key: RIB key
        bank: Bank as FK
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    account_number = models.CharField(max_length=15)
    rib_key = models.CharField(max_length=10)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)

    def __str__(self):
        return self.account_number


class FileState(models.TextChoices):
    SELECTED = "S", "Selected"
    PRECHARGED = "P", "Prechared"
    CHARGED = "C", "Charged"    


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
    date_generated = models.DateField(null=True, blank=True)
    date_updated = models.DateField(auto_now=True)


class Operation(models.Model):
    """
    Operation Model for the bank data
    Attributes:
        id: Unique id for the operation
        enrolling_nb: Enrolling number
        bank_code: Bank code
        account_number: Account number
        operation_date: Operation date
        operation_name: Operation name
        amount_credit: Amount credited or to credit
        amount_debit: Amount debited or to debit
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    enrolling_nb = models.CharField(max_length=3)
    bank_code = models.CharField(max_length=7)
    account_number = models.CharField(max_length=15)
    operation_date = models.DateField()
    operation_name = models.CharField(max_length=10)
    amount_credit = models.DecimalField(max_digits=12, decimal_places=2)
    amount_debit = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.enrolling_nb


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
