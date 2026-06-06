import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from rest_framework import viewsets

from .models import Bank, Account, BankStatementFile, Operation, Company, \
    CompanyBank
from .services import BankFileInfo, CheckFileLines, EnrolleOperations
from datetime import datetime
from bank.serializer import AccountSerializer, BankFileSerializer, \
    BankSerializer, OperationSerializer, CompanySerializer
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated
from .permissions import BankAccountPermission, FileOperationPermission

today = datetime.today()


def home(request):
    if request.user.is_authenticated and request.user.role == "V":
        return redirect('new_user')
    return render(request, 'origin/home.html', {})


def welcome(request):
    if request.user.is_authenticated:
        if request.user.role == "V":
            return redirect('new_user')
        return render(request, 'origin/welcome.html', {})
    return redirect('home')


def convert_date(name):
    return ''.join(char for char in name if char.isdigit() or char=='-')


def charge_file(request):
    """
    We will load the files before we check and charge
    their data to the database
    """
    if not request.user.is_authenticated or request.user.role == "V":
        return redirect('home')
    type_files = ['csv', 'xlsx', 'txt', 'ods', 'QET']

    if request.method == "POST":
        bank_file_info = BankFileInfo(request, 'filename', BankStatementFile)
        file_name, file_type, file = bank_file_info.file_info()

        if file_type not in type_files:
            messages.error(request, "File type not supported")
            return redirect("importdocuments/", messages)

        if bank_file_info.check_double(file_name):
            messages.error(request, "File already exists")
            return redirect("importdocuments/", messages)

        BankStatementFile.objects.create(name=file)

        response = HttpResponse()
        response["HX-Redirect"] = request.path
        return response
    return redirect("/importdocuments/")


def check_file(request):
    """
    We will check if the file is valid
    """
    file_id = None
    bank_id = None
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        file_id = data.get("file_id")
        bank_id = data.get("bank_id")

    if file_id is None or bank_id is None:
        return JsonResponse(
            {"error": "Missing file or bank"},
            status=400
        )
    bank_file = BankStatementFile.objects.get(id=file_id)
    bank = Bank.objects.get(id=bank_id)
    path = bank_file.name.path
    checked_file = CheckFileLines(path, bank_file, bank)

    if checked_file.read_file() is False:
        return JsonResponse(
            {"error": checked_file.error_message},
            status=400
        )

    return JsonResponse({
        "success": True,
        "message": "File processed successfully"
    })


def charge_data(request):
    """
    We will charge the file's checked data into
    Operations table
    """
    if not request.user.is_authenticated or request.user.role == "V":
        return redirect('home')
    file_id = None
    if request.method == "POST":
        file_id = request.POST.get("file_id")
    if file_id is None:
        messages.error(request, "Wrong file selected")
        return redirect("/importdocuments/")
    bank_file = BankStatementFile.objects.get(id=file_id)
    enrolle_operation = EnrolleOperations(bank_file,
                                          Operation,
                                          Account)
    enrolle_operation.charge_data()
    return redirect("/importdocuments/")


def bank(request):
    if request.user.is_authenticated and request.user.role == "V":
        return redirect('welcome')
    accounts, banks = None, None
    try:
        banks = Bank.objects.order_by('name')
        accounts = Account.objects.order_by('number')
        companies = Company.objects.filter(users__in=[request.user])
    except Exception as e:
        print("No data or error serializer: ", e)

    return render(request, 'bank/list_banks.html',
                  {'banks':banks, 'accounts':accounts, 'companies': companies})


def bank_form(request):
    if not request.user.is_authenticated or request.user.role == "V":
        return redirect('welcome')
    return render(request, 'bank/partials/bank_form.html')


def update_bank_form(request, bank_id):
    if bank_id is None:
        return redirect('bank')
    selected_bank = None
    if not request.user.is_authenticated or request.user.role == "V":
        return redirect('welcome')
    if bank_id:
        selected_bank = Bank.objects.get(id=bank_id)

    return render(request, "bank/partials/update_bank.html", {
        "bank": selected_bank})


def account_form(request):
    if not request.user.is_authenticated or request.user.role == "V":
        return redirect('home')
    accounts = None
    accounts = Account.objects.order_by('number')
    return render(request, 'bank/partials/account_form.html', {'accounts':accounts})


def accounts_statement(request):
    if request.user.is_authenticated and request.user.role == "V":
        return redirect('new_user')
    return render(request, 'account_statement/account_operations.html')


def importdocument(request):
    if not request.user.is_authenticated or request.user.role == "V":
        return redirect('welcome')

    if request.user.is_superuser or request.user.role == "A":
        queryset = BankStatementFile.objects.order_by('date_imported')
        serializer = BankFileSerializer(queryset, many=True)
        banks = Bank.objects.all()
        try:
            return render(request, 'import_files/files.html', {'files':queryset, 'banks':banks})
        except Exception as e:
            print("No data or error serializer: ", e)
        return render(request, 'import_files/files.html', {})
    return redirect('home')


def bank_details(request):
    bank_id = request.POST.get("bank")
    selected_bank = None
    if request.user.is_authenticated and request.user.role == "V":
        return redirect('new_user')
    if bank_id:
        selected_bank = Bank.objects.get(id=bank_id)

    return render(request, "bank/partials/bank_details.html", {
        "selected_bank": selected_bank
    })


class CompanyViewset(viewsets.ModelViewSet):
    """
    Company Viewset for managing companies
    """
    permission_classes = [IsAuthenticated]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'patch', 'delete',
                         'head', 'options']


class BankViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, BankAccountPermission]
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'patch', 'delete',
                         'head', 'options']

    def get_queryset(self):
        company = Company.objects.filter(users__in=[self.request.user])
        if company:
            return self.queryset.filter(
                company_banks__company__in=company).distinct()
        return Bank.objects.none()

    def create(self, request, *args, **kwargs):
        company_id = request.data.get("company")
        if not company_id:
            return JsonResponse(
                {"error": "company_id is required"},
                status=400
            )
        if not Company.objects.filter(id=company_id, users__in=[request.user]).exists():
            return JsonResponse(
                {"error": "You are not associated with this company"},
                status=403
            )
        company = Company.objects.get(id=company_id)
        response = super().create(request, *args, **kwargs)
        CompanyBank.objects.create(company=company,
                                   bank_id=response.data['id'],
                                   swift=response.data['swift'])

        if request.headers.get("HX-Request"):
            return render(request, "bank/partials/success_bank.html")

        return response


class AccountViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, BankAccountPermission]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'patch', 'delete',
                         'head', 'options']

    def get_queryset(self):
        return self.queryset.filter(
            bank_id=self.kwargs["bank_pk"])

    def perform_create(self, serializer):
        serializer.save(bank_id=self.kwargs["bank_pk"])


class BankFileViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, FileOperationPermission]
    queryset = BankStatementFile.objects.all()
    serializer_class = BankFileSerializer

    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'patch', 'delete',
                         'head', 'options']

    def get_queryset(self):
        pass


class OperationViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, FileOperationPermission]
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer

    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'patch', 'delete',
                         'head', 'options']

    def get_queryset(self):
        return Operation.objects.filter(
            account_id=self.kwargs["account_pk"])    

    def perform_update(self, serializer):
        pointed = serializer.validated_data.get('pointed', None)
        if pointed is not None:
            serializer.save(pointed=pointed,
                            pointer=self.request.user,
                            date_pointed=datetime.now())
        else:
            serializer.save()
    
