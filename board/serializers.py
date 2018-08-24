from rest_framework import serializers

from board.models import Free


class FreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Free
        fields = '__all__'
