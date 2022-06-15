from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import TitleViewSet, CategoryViewSet, GenreViewSet

v1_router = DefaultRouter()
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
]
