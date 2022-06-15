from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, StringRelatedField

from reviews.models import Title, Category, Genre
from rest_framework.validators import UniqueTogetherValidator
from django_filters.rest_framework import BaseInFilter, CharFilter, FilterSet


class CategorySerializer(serializers.ModelSerializer):
    # slug = SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        fields = ('name', 'slug',)
        model = Category
        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=('name', 'slug')
            )
        ]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)
        validators = [
            UniqueTogetherValidator(
                queryset=Genre.objects.all(),
                fields=('name', 'slug')
            )
        ]


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'genre', 'category'),
            )
        ]

    def validate_year(self, year):
        if year > datetime.now().year:
            from rest_framework.exceptions import ValidationError
            raise ValidationError(
                f'Нельзя вводить год больше {datetime.now().year}.')
        return year
