from django.urls import path

from . import views


urlpatterns = [
    path('confessions', views.ConfessionAPIView.as_view()),
    path('confessions/<int:confession>', views.ConfessionAPIView.as_view()),
    path('confessions/pages/<int:page>', views.ConfessionPageAPIView.as_view()),

    path('confessions/<int:confession>/likes', views.LikeAPIView.as_view()),

    path('confessions/<int:confession>/comments', views.CommentAPIView.as_view()),
    path('confessions/<int:confession>/comments/<int:comment>', views.CommentAPIView.as_view()),
    path('confessions/<int:confession>/comments/pages/<int:page>', views.CommentPageAPIView.as_view()),

    path('auth', views.AuthAPIView.as_view()),
]
