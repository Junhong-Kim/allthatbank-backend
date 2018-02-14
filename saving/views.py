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
