from rest_framework import viewsets, status
from rest_framework.response import Response

from bankbook.models import Bankbook
from bankbook.serializers import BankbookSerializer
from record.models import Record
from record.serializers import RecordSerializer


class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        # 특정 통장 내역 가져오기
        bankbook_id = self.request.query_params.get('bankbook_id', '')
        if bankbook_id:
            qs = qs.filter(bankbook_id=bankbook_id)

        return qs

    # 통장 내역 생성
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # 통장 잔액 갱신
            bankbook = Bankbook.objects.get(id=request.data['bankbook_id'])
            balance = bankbook.now_amount
            amount = int(request.data['amount'])

            if request.data['type'] == 'D':
                # 입금
                balance += amount
            elif request.data['type'] == 'W':
                # 출금
                balance -= amount

            bankbook_serializer = BankbookSerializer(bankbook, data={'now_amount': balance}, partial=True)
            if bankbook_serializer.is_valid():
                bankbook_serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
