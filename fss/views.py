import copy

from rest_framework.views import APIView

from . import services
from common.response import response_data

from rest_framework.decorators import api_view
from rest_framework.response import Response


class SavingProduct:
    def set_custom_product_data(self, product):
        options = product['options']
        custom_option_data = {
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
            custom_option_data['save_trm'].add(option['save_trm'])
            custom_option_data['rate_type'].add(option['intr_rate_type'])
            custom_option_data['rsrv_type'].add(option['rsrv_type'])

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

        custom_option_data['basic_rate']['min'] = basic_rates[-1] if basic_rates[0] == 0 else basic_rates[0]
        custom_option_data['basic_rate']['max'] = basic_rates[0] if basic_rates[-1] == 0 else basic_rates[-1]
        custom_option_data['prime_rate']['min'] = prime_rates[-1] if prime_rates[0] == 0 else prime_rates[0]
        custom_option_data['prime_rate']['max'] = prime_rates[0] if prime_rates[-1] == 0 else prime_rates[-1]

        custom_product_data = {
            'product_id': product['fin_prdt_cd'],
            'product_name': product['fin_prdt_nm'],
            'bank_id': product['fin_co_no'],
            'bank_name': product['kor_co_nm'],
            'bank_logo': 'logo.png',
            'basic_rate_min': custom_option_data['basic_rate']['min'],
            'basic_rate_max': custom_option_data['basic_rate']['max'],
            'prime_rate_min': custom_option_data['prime_rate']['min'],
            'prime_rate_max': custom_option_data['prime_rate']['max'],
            'months_6': '6' in custom_option_data['save_trm'],
            'months_12': '12' in custom_option_data['save_trm'],
            'months_24': '24' in custom_option_data['save_trm'],
            'months_36': '36' in custom_option_data['save_trm'],
            'rate_type_s': 'S' in custom_option_data['rate_type'],
            'rate_type_m': 'M' in custom_option_data['rate_type'],
            'rsrv_type_s': 'S' in custom_option_data['rsrv_type'],
            'rsrv_type_f': 'F' in custom_option_data['rsrv_type'],
            'join_way': product['join_way'],
            'join_deny': product['join_deny'],
            'join_member': product['join_member']
        }
        return custom_product_data


class SavingProductList(APIView, SavingProduct):
    def get(self, request):
        """
        전체 은행 금융상품
        """
        top_fin_grp_no = request.query_params.get('top_fin_grp_no', '020000')
        page_no = request.query_params.get('page_no', 0)
        res = services.get_saving_products(top_fin_grp_no, page_no).json()

        products = []
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
        """
        특정 은행 금융상품
        """
        fin_co_nos = request.query_params.getlist('fin_co_no')
        if len(fin_co_nos) > 0:
            deepcopy_products = copy.deepcopy(products)
            products = []
            for fin_co_no in fin_co_nos:
                for product in deepcopy_products:
                    if product['fin_co_no'] == fin_co_no:
                        products.append(product)
        # 출력 형식 변경
        custom_products = []
        for product in products:
            custom_product_data = self.set_custom_product_data(product)
            custom_products.append(custom_product_data)
        return Response(response_data(True, custom_products))


class SavingProductSearch(APIView, SavingProduct):
    def get(self, request):
        """
        전체 은행 금융상품
        """
        top_fin_grp_no = request.query_params.get('top_fin_grp_no', '020000')
        page_no = request.query_params.get('page_no', 0)
        res = services.get_saving_products(top_fin_grp_no, page_no).json()

        products = []
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
        """
        특정 상품명 검색
        """
        fin_prdt_nm = request.query_params.get('fin_prdt_nm')
        if len(fin_prdt_nm) > 0:
            deepcopy_products = copy.deepcopy(products)
            products = []
            for product in deepcopy_products:
                if fin_prdt_nm in product['fin_prdt_nm']:
                    products.append(product)
            # 출력 형식 변경
            custom_products = []
            for product in products:
                custom_product_data = self.set_custom_product_data(product)
                custom_products.append(custom_product_data)
            return Response(response_data(True, custom_products))


class SavingProductSearchOption(APIView, SavingProduct):
    def get(self, request):
        """
        전체 은행 금융상품
        """
        top_fin_grp_no = request.query_params.get('top_fin_grp_no', '020000')
        page_no = request.query_params.get('page_no', 0)
        res = services.get_saving_products(top_fin_grp_no, page_no).json()

        products = []
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
        custom_products = []
        for product in products:
            custom_product_data = self.set_custom_product_data(product)
            custom_products.append(custom_product_data)
        """
        옵션 검색
        """
        fin_co_no = request.query_params.get('fin_co_no', None)
        intr_rate_type = request.query_params.get('intr_rate_type', None)
        rsrv_type = request.query_params.get('rsrv_type', None)
        save_trm = request.query_params.get('save_trm', None)
        intr_rate = request.query_params.get('intr_rate', 0)
        intr_rate2 = request.query_params.get('intr_rate2', 0)

        # 금리 유형
        if intr_rate_type == 'S':
            param_rate_type = 'rate_type_s'
        else:
            param_rate_type = 'rate_type_m'

        # 적립 유형
        if rsrv_type == 'S':
            param_rsrv_type = 'rsrv_type_s'
        else:
            param_rsrv_type = 'rsrv_type_f'

        # 저축 기간
        if save_trm == '6':
            param_save_trm = 'months_6'
        elif save_trm == '12':
            param_save_trm = 'months_12'
        elif save_trm == '24':
            param_save_trm = 'months_24'
        else:
            param_save_trm = 'months_36'

        params = [
            ('bank_id', fin_co_no),
            (param_rate_type, intr_rate_type),
            (param_rsrv_type, rsrv_type),
            (param_save_trm, save_trm),
            ('basic_rate_max', intr_rate),
            ('prime_rate_max', intr_rate2)
        ]

        try:
            for param in params:
                custom_products = self.product_filter(custom_products, param[0], param[1])
            return Response(response_data(True, custom_products))
        except Exception as e:
            # 검색 결과가 없을 때
            return Response(response_data(True, []))

    def product_filter(self, products, param, value):
        if value is None:
            return products
        else:
            if param == 'bank_id':
                return list(filter(lambda product: product[param] == value, products))
            elif 'type' in param:
                return list(filter(lambda product: product[param] is True, products))
            elif 'months' in param:
                return list(filter(lambda product: product[param] is True, products))
            else:
                return list(filter(lambda product: float(product[param]) >= float(value), products))


@api_view(['GET'])
def companies(request):
    if request.method == 'GET':
        top_fin_grp_no = request.query_params.get('top_fin_grp_No', '020000')
        page_no = request.query_params.get('page_no', 1)

        res = services.get_companies(top_fin_grp_no, page_no).json()
        data = res['result']['baseList']
        return Response(response_data(True, data))
