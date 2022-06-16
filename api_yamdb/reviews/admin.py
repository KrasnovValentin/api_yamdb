from django.contrib import admin

from reviews.models import Category, Genre, Title, TitleGenres


class TitleGenres(admin.TabularInline):
    model = TitleGenres
    extra = 0


class TitleAdmin(admin.ModelAdmin):
    inlines = (TitleGenres,)
    list_display = ('pk',
                    'name',
                    'year',
                    'description',
                    'category',
                    )
    list_display_links = ('pk',
                          'name',
                          'year',
                          'description',
                          'category',
                          )
    list_filter = ('genre', 'category',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Category)
admin.site.register(Genre)
