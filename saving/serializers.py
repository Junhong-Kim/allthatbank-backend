from rest_framework import serializers
from .models import SavingProductBase, SavingProductOption, SavingProductBookmark


class SavingProductBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProductBase
        fields = '__all__'


class SavingProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProductOption
        fields = '__all__'


class SavingProductBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProductBookmark
        fields = '__all__'
