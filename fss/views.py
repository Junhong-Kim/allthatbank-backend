from . import services
from multiprocessing import Process

from saving.serializers import SavingProductBaseSerializer, SavingProductOptionSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def saving_products(request):
    if request.method == 'POST':
        top_fin_grp_no = request.query_params.get('topFinGrpNo', '020000')
        page_no = request.query_params.get('pageNo', '1')

        response = services.get_saving_products(top_fin_grp_no, page_no).json()
        max_page_no = int(response['result']['max_page_no']) + 1

        for now_page_no in range(1, max_page_no):
            response = services.get_saving_products(top_fin_grp_no, now_page_no).json()

            saving_products_base = response['result']['baseList']
            saving_products_option = response['result']['optionList']

            Process(target=saving_products_base_process, args=(saving_products_base, top_fin_grp_no)).start()
            Process(target=saving_products_option_process, args=(saving_products_option,)).start()

        return Response(response)


def saving_products_base_process(saving_products_base, top_fin_grp_no):
    for saving_product_base in saving_products_base:
        saving_product_base['top_fin_grp_no'] = top_fin_grp_no
        serializer = SavingProductBaseSerializer(data=saving_product_base)
        if serializer.is_valid():
            serializer.save()
        else:
            raise Exception(serializer.errors)
    return


def saving_products_option_process(saving_products_option):
    for saving_product_option in saving_products_option:
        serializer = SavingProductOptionSerializer(data=saving_product_option)
        if serializer.is_valid():
            serializer.save()
        else:
            raise Exception(serializer.errors)
    return


@api_view(['GET'])
def companies(request):
    if request.method == 'GET':
        top_fin_grp_no = request.query_params.get('topFinGrpNo', '020000')
        page_no = request.query_params.get('pageNo', 1)

        res = services.get_companies(top_fin_grp_no, page_no).json()
        return Response(res)
