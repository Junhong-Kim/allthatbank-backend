import math

from django.db.models import Q
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


class SavingProductSearch(APIView):
    def get(self, request):
        # 페이징
        offset = int(request.query_params.get('offset', 1))
        limit = int(request.query_params.get('limit', 10))

        start_index = offset * limit - limit
        end_index = offset * limit

        # 쿼리
        fin_prdt_nm = request.query_params.get('fin_prdt_nm')
        fin_co_no = request.query_params.getlist('fin_co_no')
        intr_rate_type = request.query_params.get('intr_rate_type')
        rsrv_type = request.query_params.get('rsrv_type')
        save_trm = request.query_params.get('save_trm')
        intr_rate = request.query_params.get('intr_rate', 0)
        intr_rate2 = request.query_params.get('intr_rate2', 0)

        # 상품명으로 검색
        if fin_prdt_nm:
            """
            적금상품명
            GET /saving_products/search?fin_prdt_nm=
            """
            qs = SavingProductBase.objects.all().filter(fin_prdt_nm__contains=fin_prdt_nm)
            serializer = SavingProductBaseSerializer(qs, many=True)
            products = serializer.data[start_index:end_index]

            # 검색된 적금상품 개수
            total_count = len(serializer.data)

            # 검색된 적금상품 리스트
            data = {
                'total_count': total_count,
                'max_offset_no': math.ceil(total_count / limit),
                'now_offset_no': offset,
                'products': products
            }

            return Response(data)

        # 상품옵션으로 검색
        else:
            """
            금융회사코드, 저축금리유형, 적립유형, 저축기간, 저축금리, 최고우대금리
            GET /saving_products/search?fin_co_no=&intr_rate_type=&rsrv_type=&save_trm=&intr_rate=&intr_rate2=
            """
            # 금융회사코드
            q_fin_co_no = Q()
            for f in fin_co_no:
                q_fin_co_no |= Q(fin_co_no=f)

            # 저축금리유형
            if intr_rate_type is None:
                q_intr_rate_type = Q()
            else:
                q_intr_rate_type = Q(intr_rate_type=intr_rate_type)

            # 적립유형
            if rsrv_type is None:
                q_rsrv_type = Q()
            else:
                q_rsrv_type = Q(rsrv_type=rsrv_type)

            # 검색된 적금상품 옵션
            qs = SavingProductOption.objects.all().filter(q_fin_co_no,
                                                          q_intr_rate_type,
                                                          q_rsrv_type,
                                                          save_trm=save_trm,
                                                          intr_rate__gte=intr_rate,
                                                          intr_rate2__gte=intr_rate2)
            serializer = SavingProductOptionSerializer(qs, many=True)
            options = serializer.data[start_index:end_index]

            # 검색된 적금상품 개수
            total_count = len(serializer.data)

            # 검색된 적금상품 리스트
            data = {
                'total_count': total_count,
                'max_offset_no': math.ceil(total_count / limit),
                'now_offset_no': offset,
                'products': []
            }

            # 검색된 적금상품 옵션의 상품명
            for option in options:
                saving_product_base_queryset = SavingProductBase.objects.get(fin_co_no=option['fin_co_no'],
                                                                             fin_prdt_cd=option['fin_prdt_cd'])
                saving_product_base_serializer = SavingProductBaseSerializer(saving_product_base_queryset)

                # saving_product_base_serializer.data 타입이 ReturnDict 이기 때문에 key 값 추가가 안되므로 new_dict 로 복사하여 추가
                new_dict = {}
                new_dict.update(saving_product_base_serializer.data)
                new_dict['option'] = option

                data['products'].append(new_dict)

            return Response(data)
