from django.urls import path

from . import views


urlpatterns = [
    path('confessions', views.ConfessionAPIView.as_view()),
    path('confessions/likes', views.LikeAPIView.as_view()),
    path('confessions/comments', views.CommentAPIView.as_view()),
]
