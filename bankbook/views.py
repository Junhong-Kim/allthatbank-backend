from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from bankbook.models import Bankbook
from bankbook.serializers import BankbookSerializer


class BankbookViewSet(viewsets.ModelViewSet):
    queryset = Bankbook.objects.all()
    serializer_class = BankbookSerializer

    @list_route()
    def me(self, request):
        """
        내 통장 리스트
        GET /bankbooks/me/
        """
        user_id = request.META.get('HTTP_USER_ID')
        qs = self.get_queryset().filter(user_id=user_id)
        serializer = self.get_serializer(qs, many=True)

        return Response(serializer.data)
