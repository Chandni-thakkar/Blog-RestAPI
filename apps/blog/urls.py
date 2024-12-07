# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet,basename='posts')
router.register(r'comments', CommentViewSet,basename='comments')
router.register(r'posts/(?P<slug>[-\w]+)/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),

]
