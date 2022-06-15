from django.urls import include, path
from rest_framework import routers

from .views import (
    UserViewSet, 
    send_confirmation_code, 
    send_token, 
    CommentViewSet, 
    ReviewViewSet)

router_v1 = routers.DefaultRouter()

router_v1.register('users', UserViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path(
        'v1/auth/token/',
        send_token,
        name='send_token'),
    path(
        'v1/auth/signup/',
        send_confirmation_code,
        name='send_confirmation_code'),
]
