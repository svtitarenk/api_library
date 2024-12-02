from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.response import Response
from django.db.models import Q

from library.filters import BookFilter
from library.models import Book, Author, BookIssue
from library.serializers import AuthorSerializer, BookSerializer, BookIssueSerializer
from rest_framework.permissions import IsAuthenticated


class BookViewSet(viewsets.ModelViewSet):
    """
        API для работы с книгами.
        Позволяет создавать, читать, изменять и удалять книги.
        Авторизация только для зарегистрированных пользователей.
        Позволяет сортировать по полям название, автор, жанр, пример "http://127.0.0.1:8000/books/?title=онегин"
            фильтрация не чувствительна к регистру
        Фильтрация также возможна по полю is_returned, чтобы получить только список доступных книг
        сортировка по умолчанию по полю "title", либо через параметр 'ordering'
        Пример запроса с фильтрацией и сортировкой
            "http://127.0.0.1:8000/books/?is_returned=true&ordering=-published_date"
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    # pagination_class = paginators.CustomPagination
    # filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BookFilter  # ['title', 'author__name', 'genre']
    ordering_fields = ['title', 'published_date', 'author__name']
    ordering = ['title']

    # search_fields = ('action',)
    # ordering_fields = ('frequency',)

    def perform_create(self, serializer):
        serializer.save()
        # serializer.save(user=self.request.user)  # Автоматическое назначение создателя

    def get_queryset(self):
        """
        Возвращает книги, учитывая параметр фильтрации is_returned.
        """

        queryset = Book.objects.all()

        # Проверяем наличие параметра is_returned в запросе
        is_returned = self.request.query_params.get('is_returned')
        if is_returned is not None:
            if is_returned.lower() == 'true':
                # Фильтруем книги, где все записи в BookIssue отмечены как возвращенные
                queryset = queryset.filter(
                    # Инвертируем условие ~Q(...), чтобы оставить только свободные
                    ~Q(issues__is_returned=False)  # Исключаем книги с активными записями
                ).distinct()
            elif is_returned.lower() == 'false':
                # Фильтруем книги с активными (не возвращенными) записями
                queryset = queryset.filter(
                    issues__is_returned=False
                ).distinct()

        return queryset


class AuthorViewSet(viewsets.ModelViewSet):
    """
        API для работы с авторами.
        Позволяет создавать, читать, изменять и удалять авторов.
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]


class BookIssueViewSet(viewsets.ModelViewSet):
    """
        API для работы с выдачами книг.
        Позволяет создавать, читать, изменять и удалять записи о выдачах книг.
        При возврате книги, автоматически устанавливается статус 'is_returned' в True.
        При получении книги автоматически заполняется поле выдачи текущей датой
    """

    queryset = BookIssue.objects.all()
    serializer_class = BookIssueSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()  # Создаем запись о выдаче книги

    def perform_update(self, serializer):
        # Логика обновления данных при возврате книги
        serializer.save()
