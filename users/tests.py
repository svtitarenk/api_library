from rest_framework.test import APITestCase
from rest_framework import status
from library.models import Author, Book, BookIssue
from users.models import User


class AuthorCRUDTestCase(APITestCase):
    """
        Тесты для CRUD модели Author
    """

    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create(
            email="user@example.com",
            password="password"
        )

        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

        # Создаем автора
        self.author_data = {
            "name": "Пушкин А.С.",
            "birth_date": "1799-06-06",
            "biography": "Русский поэт."
        }

        # Создаем издание книги
        self.updated_data = {
            "name": "Антон Чехов",
            "birth_date": "1860-01-29",
            "biography": "Русский драматург."
        }

    def test_create_author(self):
        response = self.client.post("/api/authors/", self.author_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 1)

    def test_read_author(self):
        author = Author.objects.create(**self.author_data)
        response = self.client.get(f"/api/authors/{author.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Пушкин А.С.")

    def test_update_author(self):
        author = Author.objects.create(**self.author_data)
        response = self.client.put(f"/api/authors/{author.id}/", self.updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Антон Чехов")

    def test_delete_author(self):
        author = Author.objects.create(**self.author_data)
        response = self.client.delete(f"/api/authors/{author.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)


class BookAuthorDuplicateTestCase(APITestCase):
    """
        Тесты для случая, когда книга с таким же автором уже существует
    """

    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create(
            email="user@example.com",
            password="password"
        )

        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

        # Создаем автора
        self.author_data = {"name": "Пушкин А.С.", "birth_date": "1799-06-06", "biography": "Русский поэт."}

        # Создаем книгу с этим автором
        self.book_data = {
            "title": "Евгений Онегин",
            "author": self.author_data,
            "genre": "Роман",
            "published_date": "1833-01-01",
            "description": "Классическое произведение."
        }

    def test_duplicate_author(self):
        # Создаем книгу, а вместе с ней и автора
        response = self.client.post("/api/books/", self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 1)

        # Пытаемся создать ту же книгу с тем же автором
        response = self.client.post("/api/books/", self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 1)  # Автор не должен быть продублирован


class BookRatingTestCase(APITestCase):
    """
        Тесты для расчета среднего рейтинга книги
    """

    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create(
            email="user@example.com",
            password="password"
        )

        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

        # Создаем автора
        self.author = Author.objects.create(
            name="Пушкин А.С.",
            birth_date="1799-06-06",
            biography="Русский поэт."
        )

        # Создаем книгу с указанием автора и пользователя
        self.book = Book.objects.create(
            title="Евгений Онегин",
            genre="Роман",
            description="Классика.",
            author=self.author,
            user=self.user  # Указываем пользователя
        )

    def test_rating_calculation(self):
        # Добавляем записи с рейтингами
        BookIssue.objects.create(book=self.book, user=self.user, rating=4, is_returned=True)
        BookIssue.objects.create(book=self.book, user=self.user, rating=5, is_returned=True)

        # Проверяем средний рейтинг через API
        response = self.client.get(f"/api/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['average_rating'], 4.5)  # Проверяем расчет рейтинга


class BookIssueReturnTestCase(APITestCase):
    """
        Тесты для возврата книги
        Дата возврата не может быть раньше даты выдачи
    """

    def setUp(self):
        # Создаем автора
        self.author = Author.objects.create(
            name="Пушкин А.С.",
            birth_date="1799-06-06",
            biography="Русский поэт."
        )

        # Создаем пользователя
        self.user = User.objects.create(
            email="user@example.com",
            password="password"
        )
        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

        # Создаем книгу с указанием автора
        self.book = Book.objects.create(
            title="Евгений Онегин",
            genre="Роман",
            description="Классика.",
            author=self.author,
            user=self.user  # Указываем пользователя
        )

    def test_invalid_return_date(self):
        # Создаем запись о выдаче книги
        issue = BookIssue.objects.create(book=self.book, user=self.user)

        # Пытаемся сдать книгу с некорректной датой возврата
        response = self.client.patch(
            f"/api/book-issues/{issue.id}/",
            {"return_date": "2023-01-01"},
            format='json'
        )

        # Проверяем, что сервер вернул ошибку
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Дата возврата не может быть раньше даты выдачи", str(response.data))


class UserBooksStatsTestCase(APITestCase):
    """
        Проверяем статистику пользователя
        Тест на количество книг, прочитанных пользователем
        и количества дней книги на руках
    """

    def setUp(self):
        # Создаем автора
        self.author = Author.objects.create(
            name="Пушкин А.С.",
            birth_date="1799-06-06",
            biography="Русский поэт."
        )

        # Создаем пользователя
        self.user = User.objects.create(
            email="user@example.com",
            password="password"
        )
        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

        # Создаем книгу с указанием автора
        self.book = Book.objects.create(
            title="Евгений Онегин",
            genre="Роман",
            description="Классика.",
            author=self.author,
            user=self.user  # Указываем пользователя
        )

    def test_user_books_stats(self):
        # Создаем запись о выдаче книги
        issue = BookIssue.objects.create(
            book=self.book,
            user=self.user,
            issue_date="2024-12-02")
        print('issue', issue)

        # Возвращаем книгу
        response = self.client.patch(
            f"/api/book-issues/{issue.id}/",
            {"return_date": "2024-12-03"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем статистику пользователя
        self.user.refresh_from_db()  # Обновляем пользователя из базы
        print(
            f"User stats after return: total_books_taken={self.user.total_books_taken}, "
            f"total_days_held_books={self.user.total_days_held_books}"
        )
        self.assertEqual(self.user.total_books_taken, 1)
        self.assertEqual(self.user.total_days_held_books, 1)  # issue.calculate_days_held()
