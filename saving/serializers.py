from rest_framework import serializers
from .models import SavingProductBase, SavingProductOption


class SavingProductBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProductBase
        fields = '__all__'


class SavingProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProductOption
        fields = '__all__'
