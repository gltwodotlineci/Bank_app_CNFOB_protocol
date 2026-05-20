

class OperationLine():
    """
    OpertaionBlock, to store the information of each line from the file
    Attributes:
        record_code (str): the record code of bank operatin
        bank_code (str): the bank code
        account_number (str): the account number
        operation_date (str): the date of operation
        label (str): the type of operation
        operation_value (float): the value of operation
        operation_description (str): the description of operation
    """
    def __init__(self, record_code:str, bank_code:str,
                 account_number:str, date:str, label:str,
                 amount:float, credit_debit:str):
        self.record_code = record_code
        self.bank_code = bank_code
        self.account_number = account_number
        self.operation_date = date
        self.label = label
        self.amount = amount
        self.credit_debit = credit_debit

    def serialize_operations(self):
        return {
            'record_code': self.record_code,
            'bank_code': self.bank_code,
            'account_number': self.account_number,
            'date': self.get_date,
            'label': self.label,
            'amount': self.get_amount,
            'credit_debit': self.credit_debit
        }

    @property
    def get_date(self):
        date = self.date

        return f"20{date[4:6]}-{date[2:4]}-{date[0:2]}"

    @property
    def get_amount(self):
        return int(self.operation_value)/100


def read_file(file_path:str, ClassOperation):
    """
    Read the file and return a list of OperationLine
    """
    credit_chars = ['{', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    debit_chars = ['}', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']

    with open(file_path, 'r', encoding='latin-1') as file:
        for raw_line  in file:
            line = raw_line.strip('\n')
            if not line.strip() or line[0:2] != '04':
                continue
            if line[103] in credit_chars:
                credit_debit = 'C'
            elif line[103] in debit_chars:
                credit_debit = 'D'


            op = OperationLine(line[0:2], line[2:7], line[21:32],
                                line[34:40], line[49:79], line[79:],
                                credit_debit)
            ClassOperation(**op.serialize_operations())
