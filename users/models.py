from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Почта', help_text='Укажите почту')
    phone = models.CharField(max_length=35, **NULLABLE, verbose_name='Телефон', help_text='Укажите телефон')
    tg_nick = models.CharField(max_length=255, **NULLABLE, verbose_name='Tg name', help_text='укажите ник телеграмм')
    avatar = models.ImageField(upload_to='users/avatar/', **NULLABLE, verbose_name='Аватар',
                               help_text='Загрузите аватар')
    total_books_taken = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество взятых книг",
        help_text="Общее количество книг, взятых пользователем"
    )
    total_days_held_books = models.PositiveIntegerField(
        default=0,
        verbose_name="Общее количество дней использования книг",
        help_text="Общее количество дней, на которые книги были взяты пользователем"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
