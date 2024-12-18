# Generated by Django 5.1.3 on 2024-12-01 16:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите имя автора', max_length=255, verbose_name='Имя автора')),
                ('birth_date', models.DateField(blank=True, help_text='Введите дату рождения', null=True, verbose_name='Дата рождения')),
                ('biography', models.TextField(blank=True, help_text='Укажите биографию автора', verbose_name='Биография автора')),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Укажите название книги', max_length=255, verbose_name='Название книги')),
                ('genre', models.CharField(help_text='Укажите жанр книги', max_length=100, verbose_name='Жанр')),
                ('published_date', models.DateField(blank=True, help_text='Дата публикации', null=True, verbose_name='Дата публикации')),
                ('description', models.TextField(blank=True, help_text='Описание книги', verbose_name='Описание')),
                ('author', models.ForeignKey(help_text='Укажите автора', on_delete=django.db.models.deletion.CASCADE, related_name='books', to='library.author', verbose_name='Автора')),
                ('user', models.ForeignKey(help_text='Пользователь, добавивший книгу', on_delete=django.db.models.deletion.CASCADE, related_name='books', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
            ],
            options={
                'verbose_name': 'Книга',
                'verbose_name_plural': 'Книги',
                'ordering': ['-title'],
            },
        ),
        migrations.CreateModel(
            name='BookIssue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateField(auto_now_add=True, help_text='Дата получения', verbose_name='Дата получения')),
                ('return_date', models.DateField(blank=True, help_text='Дата возврата', null=True, verbose_name='Дата возврата')),
                ('is_returned', models.BooleanField(default=False)),
                ('book', models.ForeignKey(help_text='Укажите книгу', on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='library.book', verbose_name='Книга')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Выдача книги',
                'verbose_name_plural': 'Выдачи книг',
                'ordering': ['-issue_date'],
            },
        ),
    ]
