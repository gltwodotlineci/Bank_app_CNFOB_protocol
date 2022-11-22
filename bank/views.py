from django.shortcuts import render, redirect
from .models import Bank, AccountNumber, ImportingDocument, FileUpload, OldAccount
from .forms import BankForm, AccountForm
from django.shortcuts import render
from datetime import datetime

today = datetime.today()

def home(request):
    return render(request, 'origin/home.html', {})

def bank(request):
    banks = Bank.objects.order_by('name_bank')
    accounts = AccountNumber.objects.order_by('account_number')
    return render(request, 'bank/list.html', {'banks':banks, 'accounts':accounts})


def importdocument(request):
    selcteddocuments = FileUpload.objects.order_by('-id')
    importdocuments = ImportingDocument.objects.order_by('-id')
    if request.method == "POST":
        file2 = request.FILES["file"]
        Lines = file2.readlines()
        for line in Lines:
            print(line)
        document = FileUpload.objects.create(file=file2, created_at=today)#, created_at=Date.today)
        document.save()
    return render(request, 'import/importdata.html', {'selcteddocuments':selcteddocuments, 'importdocuments':importdocuments})

'''
        for line in file2.readlines():
            enrolling = line[0:2]
            code_bank = line[2:7]
            old_account = OldAccount.objects.create(enrolling_nb=enrolling,
                                                    bank_code=code_bank,
                                                    account_number="abc",
                                                    date="efg",
                                                    amount_credit="100",
                                                    amount_debit="200"
                                                    )
            old_account.save
    return render(request, 'import/importdata.html', {'selcteddocuments':selcteddocuments, 'importdocuments':importdocuments})
'''

def create_class_doc(request):
    #        print(file2.readlines(10))
    pass



def select_name_doc(request):
    form = UploadFile(request.POST, request.FILES)
    file = request.FILES['file']
    return HttpResponse("str(file)")

'''
def importdata(request):
    return render(request,'import/importdata.html', {})
'''
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

class UploadFileForm(forms.Form):
    file = forms.FielField()


'''

