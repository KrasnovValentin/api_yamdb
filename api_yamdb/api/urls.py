from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import (TitleViewSet, CategoryViewSet, GenreViewSet,  
                       UserViewSet, 
    send_confirmation_code, 
    send_token, 
    CommentViewSet, 
    ReviewViewSet)

v1_router = DefaultRouter()
router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')
v1_router.register('titles', TitleViewSet, basename='titles')
# v1_router.register(r'titles/(?P<title_id>\d+)/', TitleViewSet,
#                    basename='titles')
v1_router.register('categories', CategoryViewSet, basename='categories')
# v1_router.register(r'categories/(?P<slug>\w+)/', CategoryViewSet,
#                    basename='categories')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(r'genres/(?P<slug>\w+)/', GenreViewSet,
                   basename='genres')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    # path('v1/', include('djoser.urls')),
    # path('v1/', include('djoser.urls.jwt')),
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
