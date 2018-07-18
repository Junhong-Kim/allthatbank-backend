from django.urls import path
from . import views

urlpatterns = [
    path('saving_products', views.SavingProductList.as_view()),
    path('saving_products/search', views.SavingProductSearch.as_view()),
    path('saving_products/search/option', views.SavingProductSearchOption.as_view()),
    path('companies', views.companies),
]
