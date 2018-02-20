from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from saving.models import SavingProductBase, SavingProductOption
from saving.serializers import SavingProductBaseSerializer, SavingProductOptionSerializer


class SavingProductList(APIView):
    def get(self, request):
        data = {}

        # 페이징
        offset = int(request.query_params.get('offset', 1))
        limit = int(request.query_params.get('limit', 10))

        start_index = offset * limit - limit
        end_index = offset * limit

        # 권역 코드, 금융회사 코드
        top_fin_grp_no = request.query_params.get('top_fin_grp_no')
        fin_co_no = request.query_params.get('fin_co_no')

        # 전체 적금상품 쿼리셋
        saving_products_base_queryset = SavingProductBase.objects.all()

        if top_fin_grp_no:
            """
            특정 권역 코드의 적금상품 리스트
            GET /saving_products?top_fin_grp_no=&offset=&limit=
            """
            qs = saving_products_base_queryset.filter(top_fin_grp_no=top_fin_grp_no)
            serializer = SavingProductBaseSerializer(qs, many=True)

            data['products'] = serializer.data[start_index:end_index]

        elif fin_co_no:
            """
            특정 금융회사 코드의 적금상품 리스트
            GET /saving_products?fin_co_no=&offset=&limit=
            """
            qs = saving_products_base_queryset.filter(fin_co_no=fin_co_no)
            serializer = SavingProductBaseSerializer(qs, many=True)

            data['products'] = serializer.data[start_index:end_index]

        else:
            """
            전체 적금상품 리스트
            GET /saving_products?offset=&limit=
            """
            serializer = SavingProductBaseSerializer(saving_products_base_queryset, many=True)

            data['products'] = serializer.data[start_index:end_index]

        # 적금상품 옵션
        for product in data['products']:
            fin_prdt_cd = product['fin_prdt_cd']
            saving_product_option_queryset = SavingProductOption.objects.all().filter(fin_prdt_cd=fin_prdt_cd)
            saving_product_option_serializer = SavingProductOptionSerializer(saving_product_option_queryset, many=True)

            product['options'] = saving_product_option_serializer.data

        return Response(data)


class SavingProductDetail(APIView):
    def get(self, request, fin_prdt_cd):
        """
        특정 적금상품 리스트
        GET /saving_products/{fin_prdt_cd}?fin_co_no=
        """
        try:
            data = {}

            # 금융회사 코드
            fin_co_no = request.query_params.get('fin_co_no')

            # 특정 적금상품 기본
            saving_product_base_queryset = SavingProductBase.objects.get(fin_prdt_cd=fin_prdt_cd, fin_co_no=fin_co_no)
            saving_product_base_serializer = SavingProductBaseSerializer(saving_product_base_queryset)

            # 특정 적금상품 옵션
            saving_product_option_queryset = SavingProductOption.objects.all().filter(fin_prdt_cd=fin_prdt_cd)
            saving_product_option_serializer = SavingProductOptionSerializer(saving_product_option_queryset, many=True)

            # 특정 적금상품 응답
            data['product'] = saving_product_base_serializer.data
            data['product']['options'] = saving_product_option_serializer.data

            return Response(data)
        except SavingProductBase.DoesNotExist:
            raise Http404
