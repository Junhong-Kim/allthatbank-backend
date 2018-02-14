from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from saving.models import SavingProductBase, SavingProductOption
from saving.serializers import SavingProductBaseSerializer, SavingProductOptionSerializer


class SavingProductList(APIView):
    def get(self, request):
        data = {}

        # 적금상품 기본
        saving_products_base_queryset = SavingProductBase.objects.all()
        saving_products_base_serializer = SavingProductBaseSerializer(saving_products_base_queryset, many=True)

        # 적금상품 옵션
        saving_products_option_queryset = SavingProductOption.objects.all()
        saving_products_option_serializer = SavingProductOptionSerializer(saving_products_option_queryset, many=True)

        # 적금상품 응답
        data['products'] = saving_products_base_serializer.data
        data['options'] = saving_products_option_serializer.data
        return Response(data)


class SavingProductDetail(APIView):
    def get(self, request, fin_prdt_cd):
        try:
            data = {}

            # 특정 적금상품 기본
            saving_product_base_queryset = SavingProductBase.objects.get(fin_prdt_cd=fin_prdt_cd)
            saving_product_base_serializer = SavingProductBaseSerializer(saving_product_base_queryset)

            # 특정 적금상품 옵션
            saving_product_option_queryset = SavingProductOption.objects.all().filter(fin_prdt_cd=fin_prdt_cd)
            saving_product_option_serializer = SavingProductOptionSerializer(saving_product_option_queryset, many=True)

            # 특정 적금상품 응답
            data['product'] = saving_product_base_serializer.data
            data['options'] = saving_product_option_serializer.data
            return Response(data)
        except SavingProductBase.DoesNotExist:
            raise Http404
