from rest_framework import serializers

from allthatbank.utils.cipher import AESCipher
from .models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if validated_data.get('password') is not None:
            validated_data['password'] = AESCipher().encrypt_str(validated_data['password'])
        return User.objects.create(**validated_data)

    class Meta:
        model = User
        fields = '__all__'
