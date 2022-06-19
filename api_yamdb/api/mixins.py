from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class CategModelViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet,):
    """
    Отдельный вьюсет, для вьюсета категории
    """
