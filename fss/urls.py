from django.urls import path
from . import views

urlpatterns = [
    path('saving_products', views.saving_products),
    path('companies', views.companies),
]
