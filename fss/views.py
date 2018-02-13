from . import services

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def saving_products(request):
    if request.method == 'GET':
        top_fin_grp_no = request.query_params.get('topFinGrpNo', '020000')
        page_no = request.query_params.get('pageNo', '1')

        response = services.get_saving_products(top_fin_grp_no, page_no).json()
        return Response(response)
