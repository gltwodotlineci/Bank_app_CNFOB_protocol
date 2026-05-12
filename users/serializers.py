from users.models import CustomUser, UserRole
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for UserRole
    """
    password = serializers.CharField(write_only=True)    
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
