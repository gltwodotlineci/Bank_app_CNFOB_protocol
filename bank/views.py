from django.shortcuts import render, redirect
from .models import Bank
from .models import AccountNumber
from .forms import BankForm
from .forms import AccountForm
from django.shortcuts import render
from .models import Bank, AccountNumber

def home(request):
    return render(request, 'origin/home.html', {})

def bank(request):
    banks = Bank.objects.order_by('name_bank')
    accounts = AccountNumber.objects.order_by('account_number')
    return render(request, 'bank/list.html', {'banks':banks, 'accounts':accounts})

def importdata(request):
    return render(request, 'import/importdata.html', {})

def imported_data(request):
    return render(request,'import/imported_data.html', {})

def statement_of_accounts(request):
    return render(request, 'bank/account.html', {})

def general_view(request):
    return render(request,'bank/general_view.html', {})

def createBank(request):
    form = BankForm()
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = BankForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'bank/bank_form.html', context)

def createAccount(request):
    form = AccountForm()
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_banks/')

    context = {'form': form}
    return render(request, 'bank/account_form.html', context)
'''
    banks = Bank.objects.all()
    accounts = AccountNumber.objects.all()
    account_nb = accounts.account_number
    bank = banks.bank
    iban_nb = bank.country_bank_code + banks.country_key + banks.bank_code + \
              banks.branch_code + accounts.account_number + accounts.rib_key
    context = {'name_bank': banks.name_bank,
                'bank_code':banks.bank_code ,
                'branch_code':banks.branch_code ,
                'account_number': accounts.account_number,
                'rib_key':accounts.rib_key,
                'bic':banks.bic ,
                'bank_adresse':banks.bank_adresse,
                'country_bank_code':banks.country_bank_code,
                'country_key':banks.country_key ,
                'iban':iban_nb
               }
    return render(request, 'bank/account_form.html', context)

'''

