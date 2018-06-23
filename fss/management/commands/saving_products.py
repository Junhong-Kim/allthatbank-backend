from multiprocessing import Process

from django.core.management import BaseCommand

from saving.serializers import SavingProductBaseSerializer, SavingProductOptionSerializer
from fss import services


class Command(BaseCommand):
    def handle(self, *args, **options):
        top_fin_grp_no = '020000'

        response = services.get_saving_products(top_fin_grp_no, 0).json()
        max_page_no = int(response['result']['max_page_no']) + 1

        for now_page_no in range(1, max_page_no):
            response = services.get_saving_products(top_fin_grp_no, now_page_no).json()

            saving_products_base = response['result']['baseList']
            saving_products_option = response['result']['optionList']

            Process(target=self.saving_products_base_process, args=(saving_products_base, top_fin_grp_no)).start()
            Process(target=self.saving_products_option_process, args=(saving_products_option,)).start()

    @staticmethod
    def saving_products_base_process(saving_products_base, top_fin_grp_no):
        for saving_product_base in saving_products_base:
            saving_product_base['top_fin_grp_no'] = top_fin_grp_no
            serializer = SavingProductBaseSerializer(data=saving_product_base)
            if serializer.is_valid():
                serializer.save()
            else:
                raise Exception(serializer.errors)

    @staticmethod
    def saving_products_option_process(saving_products_option):
        for saving_product_option in saving_products_option:
            serializer = SavingProductOptionSerializer(data=saving_product_option)
            if serializer.is_valid():
                serializer.save()
            else:
                raise Exception(serializer.errors)
