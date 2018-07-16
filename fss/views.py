from . import services
from common.response import response_data

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def saving_products(request):
    if request.method == 'GET':
        products = []
        top_fin_grp_no = request.query_params.get('topFinGrpNo', '020000')
        page_no = request.query_params.get('pageNo', 0)
        res = services.get_saving_products(top_fin_grp_no, page_no).json()

        for page_no in range(int(res['result']['max_page_no'])):
            res = services.get_saving_products(top_fin_grp_no, page_no + 1).json()
            product_list = res['result']['baseList']
            option_list = res['result']['optionList']

            for product in product_list:
                product['options'] = []
                for option in option_list:
                    if product['fin_prdt_cd'] == option['fin_prdt_cd']:
                        product['options'].append(option)
                products.append(product)
        return Response(response_data(True, products))


@api_view(['GET'])
def companies(request):
    if request.method == 'GET':
        top_fin_grp_no = request.query_params.get('topFinGrpNo', '020000')
        page_no = request.query_params.get('pageNo', 1)

        res = services.get_companies(top_fin_grp_no, page_no).json()
        return Response(res)
