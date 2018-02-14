from . import services
from saving.models import SavingProductBase, SavingProductOption

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def saving_products(request):
    if request.method == 'GET':
        top_fin_grp_no = request.query_params.get('topFinGrpNo', '020000')
        page_no = request.query_params.get('pageNo', '1')

        response = services.get_saving_products(top_fin_grp_no, page_no).json()

        saving_products_base = response['result']['baseList']
        saving_products_option = response['result']['optionList']

        for saving_product_base in saving_products_base:
            print(saving_product_base['kor_co_nm'])
            SavingProductBase(dcls_month=saving_product_base['dcls_month'],
                              fin_co_no=saving_product_base['fin_co_no'],
                              kor_co_nm=saving_product_base['kor_co_nm'],
                              fin_prdt_cd=saving_product_base['fin_prdt_cd'],
                              fin_prdt_nm=saving_product_base['fin_prdt_nm'],
                              join_way=saving_product_base['join_way'],
                              mtrt_int=saving_product_base['mtrt_int'],
                              spcl_cnd=saving_product_base['spcl_cnd'],
                              join_deny=saving_product_base['join_deny'],
                              join_member=saving_product_base['join_member'],
                              etc_note=saving_product_base['etc_note'],
                              max_limit=saving_product_base['max_limit'],
                              dcls_strt_day=saving_product_base['dcls_strt_day'],
                              dcls_end_day=saving_product_base['dcls_end_day'],
                              fin_co_subm_day=saving_product_base['fin_co_subm_day'],
                              top_fin_grp_no=top_fin_grp_no).save()

        for saving_product_option in saving_products_option:
            print(saving_product_option)
            SavingProductOption(dcls_month=saving_product_option['dcls_month'],
                                fin_co_no=saving_product_option['fin_co_no'],
                                fin_prdt_cd=saving_product_option['fin_prdt_cd'],
                                intr_rate_type=saving_product_option['intr_rate_type'],
                                intr_rate_type_nm=saving_product_option['intr_rate_type_nm'],
                                rsrv_type=saving_product_option['rsrv_type'],
                                rsrv_type_nm=saving_product_option['rsrv_type_nm'],
                                save_trm=saving_product_option['save_trm'],
                                intr_rate=saving_product_option['intr_rate'],
                                intr_rate2=saving_product_option['intr_rate2']).save()

        return Response(response)
