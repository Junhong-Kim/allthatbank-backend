from django.db import models


class CompanyBase(models.Model):
    class Meta:
        db_table = 'company_base'

    # 공시 제출월 [YYYYMM] **
    dcls_month = models.CharField(max_length=64)
    # 금융회사 코드 **
    fin_co_no = models.CharField(max_length=64)
    # 금융회사명
    kor_co_nm = models.CharField(max_length=64)
    # 공시 담당자
    dcls_chrg_man = models.CharField(max_length=256)
    # 홈페이지 주소
    homp_url = models.CharField(max_length=256)
    # 콜센터 전화번호
    cal_tel = models.CharField(max_length=64)
    # 권역 코드
    top_fin_grp_no = models.CharField(max_length=64)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CompanyOption(models.Model):
    class Meta:
        db_table = 'company_option'

    # 공시 제출월 [YYYYMM] **
    dcls_month = models.CharField(max_length=64)
    # 금융회사 코드 **
    fin_co_no = models.CharField(max_length=64)
    # 지역구분
    area_cd = models.CharField(max_length=64)
    # 지역이름
    area_nm = models.CharField(max_length=64)
    # 점포소재 여부
    exis_yn = models.CharField(max_length=64)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
