from django.urls import path
from . import views

urlpatterns = [
    path('saving_products', views.SavingProduct.as_view()),
    path('companies', views.companies),
]
