from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from common.response import response_data
from company.models import CompanyBase, CompanyOption
from company.serializers import CompanyBaseSerializer, CompanyOptionSerializer


class CompanyList(APIView):
    def get(self, request):
        data = {}

        # 페이징
        offset = int(request.query_params.get('offset', 1))
        limit = int(request.query_params.get('limit', 10))

        start_index = offset * limit - limit
        end_index = offset * limit

        # 권역 코드
        top_fin_grp_no = request.query_params.get('top_fin_grp_no')

        # 전체 금융회사 쿼리셋
        company_base_queryset = CompanyBase.objects.all()

        if top_fin_grp_no:
            """
            특정 권역 코드의 금융회사 리스트
            GET /company?top_fin_grp_no=&offset=&limit=
            """
            qs = company_base_queryset.filter(top_fin_grp_no=top_fin_grp_no).order_by('kor_co_nm')
            serializer = CompanyBaseSerializer(qs, many=True)

            data = serializer.data[start_index:end_index]
        else:
            """
            전체 금융회사 리스트
            GET /company?offset=&limit=
            """
            serializer = CompanyBaseSerializer(company_base_queryset, many=True)

            data = serializer.data[start_index:end_index]
        return Response(response_data(True, data))


class CompanyDetail(APIView):
    def get(self, request, fin_co_no):
        """
        특정 금융회사 상세 정보
        GET /company/{fin_co_no}
        """
        try:
            data = {}

            # 특정 금융회사 기본
            company_base_queryset = CompanyBase.objects.get(fin_co_no=fin_co_no)
            company_base_serializer = CompanyBaseSerializer(company_base_queryset)

            # 특정 금융회사 옵션
            company_option_queryset = CompanyOption.objects.all().filter(fin_co_no=fin_co_no)
            company_option_serializer = CompanyOptionSerializer(company_option_queryset, many=True)

            # 특정 적금상품 응답
            data['company'] = company_base_serializer.data
            data['company']['options'] = company_option_serializer.data

            return Response(data)
        except CompanyBase.DoesNotExist:
            raise Http404
