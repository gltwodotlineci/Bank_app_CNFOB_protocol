from rest_framework import serializers
from .models import Operation, NewBalanceAccount, BankStatementFile, Bank ,\
      AccountNumber


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
        model = AccountNumber
        fields = '__all__'
        read_only_fields = ('id',)


class OperationsSerializer(serializers.Serializer):
    class Meta:
        model = Operation


class NewBalanceAccountSerializer(serializers.Serializer):
    class Meta:
        model = NewBalanceAccount
