from rest_framework import viewsets

from bankbook.models import Bankbook
from bankbook.serializers import BankbookSerializer


class BankbookViewSet(viewsets.ModelViewSet):
    queryset = Bankbook.objects.all()
    serializer_class = BankbookSerializer
