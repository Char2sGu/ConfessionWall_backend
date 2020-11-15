from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('confessions', views.ConfessionAPIViewSet)
router.register('people', views.PersonAPIViewSet)
router.register('likes', views.LikeAPIViewSet)
router.register('comments', views.CommentAPIViewSet)

urlpatterns = [
    path('auth', views.AuthAPIView.as_view()),
]

urlpatterns += router.urls
