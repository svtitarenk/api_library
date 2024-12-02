import django_filters
from library.models import Book
from django.db.models import Q


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')  # Частичное совпадение
    author__name = django_filters.CharFilter(lookup_expr='icontains')  # Частичное совпадение
    genre = django_filters.CharFilter(lookup_expr='icontains')  # Частичное совпадение
    is_returned = django_filters.BooleanFilter(method='filter_is_returned', label='Is Returned')

    class Meta:
        model = Book
        fields = ['title', 'author__name', 'genre', 'is_returned']

    @staticmethod
    def filter_is_returned(queryset, name, value):
        """
            Фильтрация по книгам, которые не на руках
            Инвертируем условие ~Q(...), чтобы оставить только свободные
            distinct() - берем уникальные значения, чтобы исключить дубли
        """

        if value:
            return queryset.filter(~Q(issues__is_returned=False)).distinct()
        else:
            return queryset.filter(issues__is_returned=False).distinct()
