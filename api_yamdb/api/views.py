from rest_framework import viewsets, permissions, filters, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from reviews.models import Title, Genre, Category

from api.serializers import (TitleSerializer, GenreSerializer,
                             CategorySerializer)

from api.permissions import AuthorOrReadOnly


class TitleViewSet(viewsets.ModelViewSet, APIView):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = (AuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category', 'genre')
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        categ = self.request.data['category']
        category_slug = categ.get('slug')
        category = get_object_or_404(Category, slug=category_slug)
        genre_list = self.request.data['genre']
        slug_list = [slg.get('slug') for slg in genre_list]
        genres = Genre.objects.filter(slug__in=slug_list)
        serializer.save(
            category=category,
            genre=genres,
        )

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def perform_update(self, serializer):
        pass


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet,
                   mixins.DestroyModelMixin,):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('slug',)

    # def delete(self, request):
    #     slug = self.kwargs.get('slug')
    #     genre = Genre.objects.get(slug=slug)
    #     genre.delete()
    #     serializer = GenreSerializer(genre, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        genre = Genre.objects.get(slug=slug)
        lookup_field = ('slug',)
        # instance = self.get_object()
        self.perform_destroy(genre)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (AuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('slug',)
