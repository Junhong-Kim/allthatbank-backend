from rest_framework import serializers
from .models import Bankbook


class BankbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bankbook
        fields = '__all__'
