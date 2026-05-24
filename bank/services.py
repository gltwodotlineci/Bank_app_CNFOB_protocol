from uuid import UUID


class OperationLine():
    """
    OpertaionBlock, to store the information of each line from the file
    Attributes:
        record_code (str): the record code of bank operatin
        bank_code (str): the bank code
        number (str): the account number
        operation_date (str): the date of operation
        label (str): the type of operation
        amount (float): the value of operation
        operation_description (str): the description of operation
    """
    def __init__(self, record_code:str, bank_code:str,
                 number:str, operation_date:str, label:str,
                 amount:float, credit_debit:str, account):
        self.record_code = record_code
        self.bank_code = bank_code
        self.number = number
        self.date = operation_date
        self.label = label
        self.amount = amount
        self.credit_debit = credit_debit
        self.account = account

    def serialize_operations(self):
        return {
            'record_code': self.record_code,
            'bank_code': self.bank_code,
            'account': self.get_account_id,
            'date': self.get_date,
            'label': self.label,
            'amount': self.get_amount,
            'credit_or_debit': self.credit_debit
        }

    @property
    def get_date(self):
        date = self.date
        return f"20{date[4:6]}-{date[2:4]}-{date[0:2]}"

    @property
    def get_account_id(self):
        return self.account.objects.get(number=self.number)

    @property
    def get_amount(self):
        return int(self.amount)/100


class BankFileInfo:
    """
    Read the file and return a list of OperationLine
    """
    def __init__(self, request, filename:str, BankModel):
        self.request = request
        self.filename = filename
        self.BankModel = BankModel

    def file_info(self) -> tuple:
        file = self.request.FILES[self.filename]
        file_name = file.name
        file_type = file_name[-3:].lower()
        return file_name, file_type, file

    def check_double(self, file_name:str):
        path_and_name = "bank_statements/" + file_name
        return self.BankModel.objects.filter(
            name= path_and_name
        ).exists()


class EnrolleOperations:
    def __init__(self, checkedFile, classOperation, classAccont):
        self.checkedFile = checkedFile
        self.classOperation = classOperation
        self.classAccount = classAccont
    """
    Read the file and return a list of OperationLine
    """
    def last_check(self):
        if not self.checkedFile.checked:
            raise Exception("File not checked")
        return self.checkedFile


    def charge_data(self):
        """
        Read the file and return a list of OperationLine
        """
        file = self.last_check()
        bank_code = file.bank.code
        credit_debit = None
        amount = "000"
        file_path = file.name.path
        credit_chars = ['{', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        debit_chars = ['}', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']
        with open(file_path, 'r', encoding='latin-1') as f:
            for raw_line  in f:
                line = raw_line.strip('\n')
                if line[0:2] in ['04', '01', '07']:
                    amount = line[90:103]
                if line[103] in credit_chars:
                    credit_debit = 'C'
                elif line[103] in debit_chars:
                    credit_debit = 'D'
                elif line[103] not in ['C', 'D']:
                    credit_debit = 'L'
                op = OperationLine(record_code=line[0:2], bank_code=bank_code,
                                    number=line[22:33],
                                    operation_date=line[35:41], label=line[54:82],
                                    amount=amount, credit_debit=credit_debit,
                                    account=self.classAccount)
                self.classOperation.objects.create(**op.serialize_operations())
        file.archived = True
        file.save()


class CheckFileLines:
    def __init__(self, file_path:str, bank_file, bank):
        self.file_path = file_path
        self.bank_file = bank_file
        self.bank = bank
        self.record_codes = ['01', '04', '05', '07']

    def read_file(self):
        with open(self.file_path, 'r', encoding='latin-1') as file:
            for raw_line  in file:
                line = raw_line.strip('\n')
                if not line.strip():
                    continue
                if self.check_record_and_bank(line) is False:
                    return False

        self.bank_file.checked = True
        self.bank_file.bank = self.bank
        self.bank_file.save()
        return True

    def check_record_and_bank(self, line):
        accounts = self.bank.accounts.all()
        if line[0:2] not in self.record_codes:
            raise Exception('Record code not valid')
        if line[12:17] != self.bank.code:
            raise Exception('Bank not valid')
        if line[22:33] not in [account.account_number for account in accounts]:
            raise Exception('Account not valid')
