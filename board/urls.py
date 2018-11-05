from django.urls import path
from . import views

urlpatterns = [
    path('post', views.PostListAPIView.as_view()),
    path('post/<int:post_id>/comment', views.CommentListAPIView.as_view()),
    path('post/<int:post_id>/like', views.PostLikeListAPIView.as_view()),
    path('post/<int:pk>', views.PostDetailAPIView.as_view()),
    path('comment/<int:comment_id>/like', views.CommentLikeListAPIView.as_view()),
    path('comment/<int:pk>', views.CommentDetailAPIView.as_view()),
]
