from django.urls import path
from . import views

urlpatterns = [
    path('', views.SavingProductList.as_view()),
]
