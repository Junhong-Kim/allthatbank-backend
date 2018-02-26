from django.db import models

from user.models import User
from saving.models import SavingProductBase, SavingProductOption


class Bankbook(models.Model):
    class Meta:
        db_table = 'bankbooks'

    # 사용자 id
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # 적금상품 기본 id
    saving_product_base_id = models.ForeignKey(SavingProductBase, on_delete=models.CASCADE)
    # 적금상품 옵션 id
    saving_product_option_id = models.ForeignKey(SavingProductOption, on_delete=models.CASCADE)
    # 계좌번호
    account_number = models.CharField(max_length=64)
    # 납입 주기 (D: 매일, W: 매주, M: 매월)
    payment_period = models.CharField(max_length=64)
    # 납입 일 (null: 매일, W: 요일[MON|TUE|WED|THU|FRI], M: 일[1~31])
    payment_date = models.CharField(max_length=64, null=True)
    # 납입 금액 (null: 자유)
    payment_amount = models.IntegerField(default=0, null=True)
    # 적립 유형 (S: 정액적립식, F: 자유적립식)
    rsrv_type = models.CharField(max_length=64)
    # 저축 금리 유형 (S: 단리, M: 복리)
    intr_rate_type = models.CharField(max_length=64)
    # 기본 금리 (null: 기본 금리 없음)
    intr_rate = models.FloatField(null=True)
    # 우대 금리 (null: 우대 금리 없음)
    prime_rate = models.FloatField(null=True)
    # 현재 납입 금액
    now_amount = models.IntegerField(default=0)
    # 최대 납입 금액 (null: 제한 없음)
    max_amount = models.IntegerField(null=True)
    # 가입일 [YYYYMMDD]
    join_date = models.CharField(max_length=64)
    # 만기일 [YYYYMMDD]
    expiry_date = models.CharField(max_length=64)
    # 만기유무 (Y: 만기됨, N: 진행중, C: 해지됨)
    is_expired = models.CharField(max_length=64)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
