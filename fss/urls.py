from django.urls import path
from . import views

urlpatterns = [
    path('saving_products', views.SavingProductList.as_view()),
    path('saving_products/search', views.SavingProductSearch.as_view()),
    path('saving_products/search/option', views.SavingProductSearchOption.as_view()),
    path('saving_products/<str:fin_prdt_cd>', views.SavingProductDetail.as_view()),
    path('deposit_products', views.DepositProductList.as_view()),
    path('companies', views.companies),
]
