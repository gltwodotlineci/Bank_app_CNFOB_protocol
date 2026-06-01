from rest_framework import serializers
from .models import Operation, NewBalanceAccount, BankStatementFile, Bank ,\
      Account, Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ('id',)


class BankFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankStatementFile
        fields = '__all__'
        read_only_fields = ('id', 'name', 'date_generated', 'date_imported', 'date_updated')


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'
        read_only_fields = ('id',)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ('id',)
      

class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = '__all__'
        read_only_fields = ('id',)


class NewBalanceAccountSerializer(serializers.Serializer):
    class Meta:
        model = NewBalanceAccount
