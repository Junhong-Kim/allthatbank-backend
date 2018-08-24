from django.urls import path
from . import views

urlpatterns = [
    path('free', views.FreeList.as_view()),
    path('free/<int:pk>', views.FreeDetail.as_view()),
]
