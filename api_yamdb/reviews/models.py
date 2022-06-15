from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()

    def __str__(self):
        return f'{self.name}:{self.slug}'


class Genre(models.Model):
    name = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.name}:{self.slug}'


class TitleGenres(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True,
                              verbose_name='Жанр')
    title = models.ForeignKey('Title', on_delete=models.SET_NULL, null=True,
                              verbose_name='Название произведения')


class Title(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Название произведения')
    year = models.IntegerField(verbose_name='Год', )
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание произведения')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Категория',
        help_text='Выберите категорию'
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenres',
        related_name='titles',
        blank=True,
        verbose_name='Жанр',
        help_text='Выберите жанр'
    )

    def __str__(self):
        return self.name
