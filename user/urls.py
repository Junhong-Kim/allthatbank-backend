from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserList.as_view()),
    path('<int:pk>', views.UserDetail.as_view()),
    path('debug_token/fb', views.DebugFbToken.as_view()),
]
