from django.shortcuts import render, redirect
from .models import Bank
from .forms import BankForm
from .forms import AccountForm

def home(request):
    return render(request, 'origin/home.html', {})

def bank(request):
    return render(request, 'bank/list.html', {})

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
            return redirect('/')

    context = {'form': form}
    return render(request, 'bank/account_form.html', context)
