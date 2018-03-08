from django.urls import path
from . import views

urlpatterns = [
    path('', views.SavingProductList.as_view()),
    path('search', views.SavingProductSearch.as_view()),
    path('bookmarks', views.SavingProductBookmarkList.as_view()),
    path('bookmarks/<int:pk>', views.SavingProductBookmarkDetail.as_view()),
    path('<str:fin_prdt_cd>', views.SavingProductDetail.as_view()),
]
