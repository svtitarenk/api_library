from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "total_books_taken",
            "total_days_held_books",
            "date_joined",
            "groups",
            "is_staff",
            "password",
            "last_login",
            "is_superuser",
            "is_active",
            "phone",
            "tg_nick",
        )
