from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, send_confirmation_code, send_token

router = routers.DefaultRouter()

router.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        'v1/auth/token/',
        send_token,
        name='send_token'),
    path(
        'v1/auth/signup/',
        send_confirmation_code,
        name='send_confirmation_code'),
]
