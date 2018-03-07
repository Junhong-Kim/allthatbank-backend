from django.db import models

from bankbook.models import Bankbook
from user.models import User


class Record(models.Model):
    class Meta:
        db_table = 'records'

    # 사용자 id
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 통장 id
    bankbook = models.ForeignKey(Bankbook, on_delete=models.CASCADE)
    # 타입 (D: 입금, W: 출금)
    type = models.CharField(max_length=32)
    # 금액
    amount = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
