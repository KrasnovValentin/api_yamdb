from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from api_yamdb.settings import WORD_COUNT


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(verbose_name='URL slug', unique=True)

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    name = models.CharField(max_length=200, )
    slug = models.SlugField(verbose_name='URL slug', unique=True)

    def __str__(self):
        return f'{self.name}'


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
        related_name='titles',
        blank=True,
        verbose_name='Жанр',
        help_text='Выберите жанр'
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Введите текст отзыва'
    )
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва')
    title = models.ForeignKey(Title,
                              blank=True,
                              null=True,
                              on_delete=models.SET_NULL,
                              related_name='reviews',
                              verbose_name='Произведение',
                              help_text='Произведение, к '
                                        'которому относится отзыв')

    score = models.IntegerField(
        verbose_name='Рейтинг',

        validators=[MinValueValidator(1, message='Значение '
                                                 'должно быть больше 1'),
                    MaxValueValidator(10,
                                      message='Значение должно быть '
                                              'меньше 10')])

    def __str__(self):
        return self.text[:WORD_COUNT]

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review')]


class Comment(models.Model):
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комметария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария')
    Review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Отзыв, к которому относится комментарий')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)
