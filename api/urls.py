from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .accounts.views import UserViewSet

router = DefaultRouter()

router.register('accounts', UserViewSet, basename='accounts')

urlpatterns = [
    path('', include(router.urls)),
]
