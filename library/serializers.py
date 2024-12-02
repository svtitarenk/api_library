from rest_framework import serializers
from library.models import Author, Book, BookIssue


class AuthorSerializer(serializers.ModelSerializer):
    """
        Отображает авторов и позволяет создавать новых авторов
    """

    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    """ Отображает книги, рейтинг, автора (словарь) и пользователя, который добавил книгу в библиотеку
        Позволяет обновлять книгу
        Позволяет добавлять книгу сразу с автором, если ранее он не добавлен
        get_average_rating - выводит средний рейтинг по книгам, которые возвращены
            рейтинг рассчитывается в модели Book
    """

    author = AuthorSerializer()  # Позволяет отправлять данные автора
    user = serializers.ReadOnlyField(source="user.email", )
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'
        ordering = '-title'

    def create(self, validated_data):
        author_data = validated_data.pop('author')  # Извлекаем данные автора
        author, _ = Author.objects.get_or_create(**author_data)  # Создаем автора, если его нет

        # Получаем пользователя из контекста
        user = self.context['request'].user

        # Создаем книгу с привязкой к пользователю
        book = Book.objects.create(author=author, user=user, **validated_data)  # Создаем книгу
        return book

    def update(self, instance, validated_data):
        # Извлекаем данные автора, если они есть
        author_data = validated_data.pop('author', None)
        if author_data:
            author, _ = Author.objects.get_or_create(**author_data)
            instance.author = author  # Обновляем автора

        # Обновляем остальные поля книги
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def get_average_rating(self, obj):
        return round(obj.calculate_average_rating(), 2)  # Округляем до 2 знаков


class BookIssueSerializer(serializers.ModelSerializer):
    """
        Отображает историю выдачи книги, а также пользователя, который выдал книгу
        Дата выдачи книги присваивается автоматически моделью
        is_returned меняется также автоматически, если отмечена дата возврата книги и она позже даты выдачи
        Позволяет изменять рейтинг книги, если он указан (опционально)
    """
    book_title = serializers.CharField(source='book.title', read_only=True)  # Название книги
    user_email = serializers.EmailField(source='user.email', read_only=True)  # Email пользователя

    class Meta:
        model = BookIssue
        fields = ['id', 'book', 'book_title', 'user', 'user_email', 'issue_date', 'return_date', 'is_returned', 'rating']
        read_only_fields = ['is_returned', 'issue_date']
        ordering = '-return_date'

    def validate(self, data):
        if 'return_date' in data:
            if self.instance and data['return_date'] < self.instance.issue_date:
                raise serializers.ValidationError("Дата возврата не может быть раньше даты выдачи.")
        return data

    def update(self, instance, validated_data):
        if 'return_date' in validated_data and not instance.is_returned:
            # Если return_date указано, обновляем is_returned и пользователя
            instance.return_date = validated_data['return_date']
            instance.is_returned = True

            # Обновляем статистику пользователя
            user = instance.user
            days_held = instance.calculate_days_held()
            user.total_books_taken += 1
            user.total_days_held_books += days_held
            user.save()

        # Обновляем рейтинг, если он указан
        if 'rating' in validated_data:
            instance.rating = validated_data['rating']

        instance.save()
        return instance
