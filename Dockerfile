# Используем базовый образ Python
FROM python:3.12

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем файл зависимостей Poetry
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости (без создания виртуального окружения)
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Копируем остальной код
COPY . .

# Открываем порт
EXPOSE 8000

# Команда для запуска сервера
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
