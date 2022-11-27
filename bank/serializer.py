from rest_framework import serializers
from .models import OldAccount, Operation, NewBalanceAccount

class OldAccountSerializer(serializers.Serializer):
    class Meta:
        model = OldAccount
        fields = __all__

class OperationsSerializer(serializers.Serializer):
    class Meta:
        model = Operation
        fields = __all__


class NewBalanceAccountSerializer(serializers.Serializer):
    class Meta:
        model = NewBalanceAccount
        fields = __all__