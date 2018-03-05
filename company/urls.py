from django.urls import path
from . import views

urlpatterns = [
    path('', views.CompanyList.as_view())
]
