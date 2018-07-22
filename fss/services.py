import requests
from django.conf import settings


def get_saving_products(top_fin_grp_no, page_no):
    url = settings.SAVING_PRODUCTS_API
    params = {
        'auth': settings.FSS_AUTHENTICATION_KEY,
        'topFinGrpNo': top_fin_grp_no,
        'pageNo': page_no
    }

    response = requests.get(url, params=params)
    return response


def get_companies(top_fin_grp_no, page_no):
    url = settings.COMPANY_API
    params = {
        'auth': settings.FSS_AUTHENTICATION_KEY,
        'topFinGrpNo': top_fin_grp_no,
        'pageNo': page_no
    }

    response = requests.get(url, params=params)
    return response
