from django.db import models
from django.conf import settings
from django.db.models import Avg

NULLABLE = {"null": True, "blank": True}


class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя автора", help_text="Введите имя автора")
    birth_date = models.DateField(**NULLABLE, verbose_name="Дата рождения", help_text="Введите дату рождения")
    biography = models.TextField(blank=True, verbose_name="Биография автора", help_text="Укажите биографию автора")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ["-name"]

    def __str__(self):
        return self.name


class Book(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="books",
        verbose_name="Создатель",
        help_text="Пользователь, добавивший книгу"
    )
    title = models.CharField(max_length=255, verbose_name='Название книги', help_text="Укажите название книги")
    author = models.ForeignKey(Author, on_delete=models.CASCADE,
                               verbose_name="Автора",
                               help_text="Укажите автора",
                               related_name="books")
    genre = models.CharField(max_length=100, verbose_name="Жанр", help_text="Укажите жанр книги")
    published_date = models.DateField(verbose_name="Дата публикации", help_text="Дата публикации", **NULLABLE)
    description = models.TextField(verbose_name="Описание", help_text="Описание книги", blank=True)

    def calculate_average_rating(self):
        return self.issues.filter(is_returned=True).aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ["-title"]

    def __str__(self):
        return self.title


class BookIssue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга", help_text="Укажите книгу",
                             related_name="issues")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="issues")
    issue_date = models.DateField(auto_now_add=True, verbose_name="Дата получения", help_text="Дата получения")
    return_date = models.DateField(**NULLABLE, verbose_name="Дата возврата", help_text="Дата возврата")
    is_returned = models.BooleanField(default=False)
    rating = models.PositiveIntegerField(**NULLABLE,
                                         verbose_name="Рейтинг",
                                         help_text="От 1 до 5, где 5 высшая оценка"
                                         )

    class Meta:
        verbose_name = "Выдача книги"
        verbose_name_plural = "Выдачи книг"
        ordering = ["-issue_date"]

    def calculate_days_held(self):
        """Вычислить количество дней, которые книга была у пользователя."""
        if self.return_date and self.issue_date:
            return max((self.return_date - self.issue_date).days, 1)  # Минимум 1 день
        return 0

    def __str__(self):
        return f"{self.book.title} issued to {self.user.email}"
