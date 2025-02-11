from django.urls import path , include 
from rest_framework.router import DefaultRouter 
from .views import UserViewSet


router = DefaultRouter()
router.register(r'User', UserViewSet)

urlpatterns = [
    path('',include(router.urls)),
]