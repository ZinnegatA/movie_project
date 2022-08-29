from django.contrib import admin
from .models import Movie, Director, Actor, DressingRoom
from django.db.models import QuerySet

# Register your models here.
admin.site.register(Director)
admin.site.register(Actor)
admin.site.register(DressingRoom)


class RatingFilter(admin.SimpleListFilter):
    title = 'Фильтр по рейтингу'
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return [
            ('<40', 'Низкий'),
            ('От 40 до 59', 'Средний'),
            ('От 60 до 79', 'Высокий'),
            ('>=80', 'Высочайший')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<40':
            return queryset.filter(rating__lt=40)
        elif self.value() == 'От 40 до 59':
            return queryset.filter(rating__gte=40).filter(rating__lt=60)
        elif self.value() == 'От 60 до 79':
            return queryset.filter(rating__gte=60).filter(rating__lt=80)
        elif self.value() == '>=80':
            return queryset.filter(rating__gte=80)
        return queryset


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'rating', 'year', 'director', 'budget', 'rating_status']
    list_editable = ['rating', 'year', 'budget', 'director']
    ordering = ['-rating', 'name']
    list_per_page = 5
    actions = ['set_dollars', 'set_euros', 'set_rubles']
    search_fields = ['name']
    list_filter = ['name', 'currency', RatingFilter]

    @admin.display(ordering='rating', description='Статус')
    def rating_status(self, movie: Movie):
        if movie.rating < 50:
            return 'Зачем это смотреть?'
        elif movie.rating < 70:
            return 'Разок можно глянуть'
        elif movie.rating <= 85:
            return 'Зачет'
        else:
            return 'Топчик'

    @admin.action(description='Установить валюту в доллар')
    def set_dollars(self, request, qs: QuerySet):
        count_updated = qs.update(currency=Movie.USD)
        self.message_user(request, f'Было обновлено {count_updated} записей')

    @admin.action(description='Установить валюту в евро')
    def set_euros(self, request, qs: QuerySet):
        count_updated = qs.update(currency=Movie.EURO)
        self.message_user(request, f'Было обновлено {count_updated} записей')

    @admin.action(description='Установить валюту в рубль')
    def set_rubles(self, request, qs: QuerySet):
        count_updated = qs.update(currency=Movie.RUB)
        self.message_user(request, f'Было обновлено {count_updated} записей')
