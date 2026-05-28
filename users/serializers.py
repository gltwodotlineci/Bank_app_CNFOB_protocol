from users.models import CustomUser, UserRole
from rest_framework import serializers
from bank.models import Company


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for UserRole
    """
    password = serializers.CharField(write_only=True)
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = CustomUser
        fields = '__all__'
        read_only_fields = ('id',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        company = validated_data.pop("company", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if company:
            company.users.add(instance)

        return instance


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()
