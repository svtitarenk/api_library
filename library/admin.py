from django.contrib import admin

from library.models import Book, Author, BookIssue


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_filter = (
        'id',
        'title',
        'author',
        'published_date',
        'genre',
    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_filter = (
        'id',
        'name',
        'birth_date',
        'biography',
    )


@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'book',
        'user',
        'issue_date',
        'return_date',
        'is_returned',
        'rating'
    )
