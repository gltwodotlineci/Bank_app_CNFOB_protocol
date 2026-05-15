from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import Bank, AccountNumber, BankStatementFile
from .forms import BankForm, AccountForm
from datetime import datetime
from bank.serializer import BankFileSerializer, BankSerializer
from django.contrib import messages


today = datetime.today()

def home(request):
    return render(request, 'origin/home.html', {})


def welcome(request):
    return render(request, 'origin/welcome.html', {})


def convert_date(name):
    return ''.join(char for char in name if char.isdigit() or char=='-')


def charge_file(request):
    type_files = ['csv', 'xlsx', 'txt', 'ods', 'QET']

    if request.method == "POST":
        file = request.FILES.getlist('filename')
        file_name = file[0].name
        file_type = file_name.split('.')[-1].lower()
        if not file_type in type_files:
            messages.error(request, "File type not supported")
            return redirect("importdocuments/")
        queryset = BankStatementFile.objects.all()
        if queryset.filter(name=file_name).exists():
            messages.error(request, "File already exists")
            return redirect("importdocuments/")
        BankStatementFile.objects.create(name=file_name, archived=False)
        response = HttpResponse()
        response["HX-Redirect"] = request.path
        return response
    return redirect("/importdocuments/")    

def bank(request):
    banks = Bank.objects.order_by('name')
    accounts = AccountNumber.objects.order_by('account_number')
    return render(request, 'bank/list_banks.html', {'banks':banks, 'accounts':accounts})


def bank_form(request):
    banks = Bank.objects.order_by('name')
    return render(request, 'bank/partials/bank_form.html', {'banks':banks})


def account_form(request):
    accounts = AccountNumber.objects.order_by('account_number')
    return render(request, 'bank/partials/account_form.html', {'accounts':accounts})


def importdocument(request):
    queryset = BankStatementFile.objects.order_by('date_imported')
    serializer = BankFileSerializer(queryset, many=True)
    try:
        return render(request, 'import_files/files.html', {'files':queryset})
    except Exception as e:
        print("No data or error serializer: ", e)
    return render(request, 'import_files/files.html', {})


class BankFileViewset(viewsets.ModelViewSet):
    queryset = BankStatementFile.objects.all()
    serializer_class = BankFileSerializer

    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'patch', 'delete',
                         'head', 'options']


class BankViewset(viewsets.ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'patch', 'delete',
                         'head', 'options']


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
    form = BankStatementFile(request.POST, request.FILES)
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

