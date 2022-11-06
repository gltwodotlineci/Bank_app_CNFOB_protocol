from django.shortcuts import render

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
