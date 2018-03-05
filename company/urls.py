from django.urls import path
from . import views

urlpatterns = [
    path('', views.CompanyList.as_view()),
    path('<str:fin_co_no>', views.CompanyDetail.as_view()),
]
