from django.core.paginator import Paginator


def paging_data(qs, limit, page):
    paginator = Paginator(qs, limit)
    return paginator.page(page)
