from multiprocessing import Process

from django.core.management import BaseCommand

from company.serializers import CompanyBaseSerializer, CompanyOptionSerializer
from fss import services


class Command(BaseCommand):
    def handle(self, *args, **options):
        top_fin_grp_no = '020000'

        response = services.get_company(top_fin_grp_no, 0).json()
        max_page_no = int(response['result']['max_page_no']) + 1

        for now_page_no in range(1, max_page_no):
            response = services.get_company(top_fin_grp_no, now_page_no).json()

            company_base = response['result']['baseList']
            company_option = response['result']['optionList']

            Process(target=self.company_base_process, args=(company_base, top_fin_grp_no)).start()
            Process(target=self.company_option_process, args=(company_option,)).start()

    @staticmethod
    def company_base_process(company_base, top_fin_grp_no):
        for company_base_obj in company_base:
            company_base_obj['top_fin_grp_no'] = top_fin_grp_no
            serializer = CompanyBaseSerializer(data=company_base_obj)
            if serializer.is_valid():
                serializer.save()
            else:
                raise Exception(serializer.errors)

    @staticmethod
    def company_option_process(company_option):
        for company_option_obj in company_option:
            serializer = CompanyOptionSerializer(data=company_option_obj)
            if serializer.is_valid():
                serializer.save()
            else:
                raise Exception(serializer.errors)
