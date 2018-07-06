import math

from django.db.models import Q
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.response import response_data
from company.models import CompanyBase
from saving.models import SavingProductBase, SavingProductOption, SavingProductBookmark
from saving.serializers import SavingProductBaseSerializer, SavingProductOptionSerializer, SavingProductBookmarkSerializer


class SavingProduct(object):
    def set_options_data(self, options):
        option_data = {
            'basic_rate': {},
            'prime_rate': {},
            'save_trm': set(),
            'rate_type': set(),
            'rsrv_type': set()
        }

        basic_rates = []
        prime_rates = []

        for option in options:
            basic_rates.append(option['intr_rate'])
            prime_rates.append(option['intr_rate2'])
            option_data['save_trm'].add(option['save_trm'])
            option_data['rate_type'].add(option['intr_rate_type'])
            option_data['rsrv_type'].add(option['rsrv_type'])

        # 기본금리가 null 값인 경우 0으로 초기화
        for (index, basic_rate) in enumerate(basic_rates):
            if basic_rate is None:
                basic_rates[index] = 0

        # 우대금리가 null 값인 경우 0으로 초기화
        for (index, prime_rate) in enumerate(prime_rates):
            if prime_rate is None:
                prime_rates[index] = 0

        basic_rates = sorted(basic_rates, key=float)
        prime_rates = sorted(prime_rates, key=float)

        option_data['basic_rate']['min'] = basic_rates[-1] if basic_rates[0] == 0 else basic_rates[0]
        option_data['basic_rate']['max'] = basic_rates[0] if basic_rates[-1] == 0 else basic_rates[-1]
        option_data['prime_rate']['min'] = prime_rates[-1] if prime_rates[0] == 0 else prime_rates[0]
        option_data['prime_rate']['max'] = prime_rates[0] if prime_rates[-1] == 0 else prime_rates[-1]

        return option_data


class SavingProductList(APIView, SavingProduct):
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
            data = serializer.data[start_index:end_index]
        elif fin_co_no:
            """
            특정 금융회사 코드의 적금상품 리스트
            GET /saving_products?fin_co_no=&fin_co_no=offset=&limit=
            """
            data = []
            fin_co_nos = request.query_params.getlist('fin_co_no')
            for fin_co_no in fin_co_nos:
                qs = saving_products_base_queryset.filter(fin_co_no=fin_co_no)
                serializer = SavingProductBaseSerializer(qs, many=True)
                data += serializer.data
            data = data[start_index:end_index]

            # 적금상품 옵션
            for product in data:
                fin_prdt_cd = product['fin_prdt_cd']
                saving_product_option_queryset = SavingProductOption.objects.all().filter(fin_prdt_cd=fin_prdt_cd)
                saving_product_option_serializer = SavingProductOptionSerializer(saving_product_option_queryset,
                                                                                 many=True)
                product['options'] = saving_product_option_serializer.data

            products = []
            for product in data:
                company = CompanyBase.objects.get(fin_co_no=product['fin_co_no'])
                options = product['options']
                options_data = self.set_options_data(options)

                product_data = {
                    'id': product['fin_prdt_cd'],
                    'bank_logo': 'logo.png',
                    'bank_name': company.kor_co_nm,
                    'join_way': product['join_way'],
                    'product_name': product['fin_prdt_nm'],
                    'basic_rate_min': options_data['basic_rate']['min'],
                    'basic_rate_max': options_data['basic_rate']['max'],
                    'prime_rate_min': options_data['prime_rate']['min'],
                    'prime_rate_max': options_data['prime_rate']['max'],
                    'months_06': '6' in options_data['save_trm'],
                    'months_12': '12' in options_data['save_trm'],
                    'months_24': '24' in options_data['save_trm'],
                    'months_36': '36' in options_data['save_trm'],
                    'rate_type_s': 'S' in options_data['rate_type'],
                    'rate_type_m': 'M' in options_data['rate_type'],
                    'rsrv_type_s': 'S' in options_data['rsrv_type'],
                    'rsrv_type_f': 'F' in options_data['rsrv_type'],
                    'join_deny': product['join_deny'],
                    'join_member': product['join_member']
                }
                products.append(product_data)
            return Response(response_data(True, products))
        else:
            """
            전체 적금상품 리스트
            GET /saving_products?offset=&limit=
            """
            serializer = SavingProductBaseSerializer(saving_products_base_queryset, many=True)
            data = serializer.data[start_index:end_index]

        # 적금상품 옵션
        for product in data:
            fin_prdt_cd = product['fin_prdt_cd']
            saving_product_option_queryset = SavingProductOption.objects.all().filter(fin_prdt_cd=fin_prdt_cd)
            saving_product_option_serializer = SavingProductOptionSerializer(saving_product_option_queryset, many=True)

            product['options'] = saving_product_option_serializer.data

        return Response(response_data(True, data))


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


class SavingProductSearch(APIView, SavingProduct):
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
            data = serializer.data[start_index:end_index]

            # 적금상품 옵션
            for product in data:
                fin_prdt_cd = product['fin_prdt_cd']
                saving_product_option_queryset = SavingProductOption.objects.all().filter(fin_prdt_cd=fin_prdt_cd)
                saving_product_option_serializer = SavingProductOptionSerializer(saving_product_option_queryset,
                                                                                 many=True)
                product['options'] = saving_product_option_serializer.data

            products = []
            for product in data:
                company = CompanyBase.objects.get(fin_co_no=product['fin_co_no'])
                options = product['options']
                options_data = self.set_options_data(options)

                product_data = {
                    'id': product['fin_prdt_cd'],
                    'bank_logo': 'logo.png',
                    'bank_name': company.kor_co_nm,
                    'join_way': product['join_way'],
                    'product_name': product['fin_prdt_nm'],
                    'basic_rate_min': options_data['basic_rate']['min'],
                    'basic_rate_max': options_data['basic_rate']['max'],
                    'prime_rate_min': options_data['prime_rate']['min'],
                    'prime_rate_max': options_data['prime_rate']['max'],
                    'months_06': '6' in options_data['save_trm'],
                    'months_12': '12' in options_data['save_trm'],
                    'months_24': '24' in options_data['save_trm'],
                    'months_36': '36' in options_data['save_trm'],
                    'rate_type_s': 'S' in options_data['rate_type'],
                    'rate_type_m': 'M' in options_data['rate_type'],
                    'rsrv_type_s': 'S' in options_data['rsrv_type'],
                    'rsrv_type_f': 'F' in options_data['rsrv_type'],
                    'join_deny': product['join_deny'],
                    'join_member': product['join_member']
                }
                products.append(product_data)
            return Response(response_data(True, products))

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


class SavingProductBookmarkList(APIView):
    def get(self, request):
        qs = SavingProductBookmark.objects.all()

        # 특정 사용자 적금북마크 가져오기
        user_id = request.query_params.get('user_id')
        if user_id:
            qs = qs.filter(user_id=user_id)

        serializer = SavingProductBookmarkSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SavingProductBookmarkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SavingProductBookmarkDetail(APIView):
    def get_object(self, pk):
        try:
            return SavingProductBookmark.objects.get(pk=pk)
        except SavingProductBookmark.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        bookmark = self.get_object(pk)
        serializer = SavingProductBookmarkSerializer(bookmark)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        bookmark = self.get_object(pk)
        bookmark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
