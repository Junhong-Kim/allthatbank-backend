from rest_framework.response import Response
from rest_framework.views import APIView

from company.models import CompanyBase
from company.serializers import CompanyBaseSerializer


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
            qs = company_base_queryset.filter(top_fin_grp_no=top_fin_grp_no)
            serializer = CompanyBaseSerializer(qs, many=True)

            data['company'] = serializer.data[start_index:end_index]

        else:
            """
            전체 금융회사 리스트
            GET /company?offset=&limit=
            """
            serializer = CompanyBaseSerializer(company_base_queryset, many=True)

            data['company'] = serializer.data[start_index:end_index]

        return Response(data)
