from django.db import models

from user.models import User


class SavingProductBase(models.Model):
    class Meta:
        db_table = 'saving_products_base'

    # 공시 제출월 [YYYYMM] **
    dcls_month = models.CharField(max_length=64)
    # 금융회사 코드 **
    fin_co_no = models.CharField(max_length=64)
    # 금융회사명
    kor_co_nm = models.CharField(max_length=64)
    # 금융상품 코드 **
    fin_prdt_cd = models.CharField(max_length=64)
    # 금융상풍명
    fin_prdt_nm = models.CharField(max_length=64)
    # 가입방법
    join_way = models.CharField(max_length=64)
    # 만기 후 이자율
    mtrt_int = models.CharField(max_length=256)
    # 우대조건
    spcl_cnd = models.CharField(max_length=256)
    # 가입제한 (1: 제한없음, 2:서민전용, 3:일부제한)
    join_deny = models.CharField(max_length=64)
    # 가입대상
    join_member = models.CharField(max_length=256)
    # 기타 유의사항
    etc_note = models.CharField(max_length=256)
    # 최고한도
    max_limit = models.BigIntegerField(null=True)
    # 공시 시작일
    dcls_strt_day = models.CharField(max_length=64)
    # 공시 종료일
    dcls_end_day = models.CharField(max_length=64, null=True)
    # 금융회사 제출일 [YYYYMMDDHH24MI]
    fin_co_subm_day = models.CharField(max_length=64)
    # 권역 코드
    top_fin_grp_no = models.CharField(max_length=64)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SavingProductOption(models.Model):
    class Meta:
        db_table = 'saving_products_option'

    # 공시 제출월 [YYYYMM] **
    dcls_month = models.CharField(max_length=64)
    # 금융회사 코드 **
    fin_co_no = models.CharField(max_length=64)
    # 금융상품 코드 **
    fin_prdt_cd = models.CharField(max_length=64)
    # 저축 금리 유형 (S: 단리, M: 복리)
    intr_rate_type = models.CharField(max_length=64)
    # 저축 금리 유형명
    intr_rate_type_nm = models.CharField(max_length=64)
    # 적립 유형 (S: 정액적립식, F: 자유적립식)
    rsrv_type = models.CharField(max_length=64)
    # 적립 유형명
    rsrv_type_nm = models.CharField(max_length=64)
    # 저축 기간 [단위:개월]
    save_trm = models.CharField(max_length=64)
    # 저축 금리 [소수정 2자리]
    intr_rate = models.FloatField(null=True)
    # 최고 우대금리 [소수점 2자리]
    intr_rate2 = models.FloatField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SavingProductBookmark(models.Model):
    class Meta:
        db_table = 'saving_products_bookmark'

    # 사용자 id
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 적금상품 기본 id
    saving_product_base = models.ForeignKey(SavingProductBase, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
