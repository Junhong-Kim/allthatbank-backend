from rest_framework import serializers
from .models import CompanyBase, CompanyOption


class CompanyBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyBase
        fields = '__all__'


class CompanyOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyOption
        fields = '__all__'
