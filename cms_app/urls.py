from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', Userview, basename='user')
router.register(r'blog', Blogview, basename='blog')
router.register(r'like', Likeview, basename='like')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]