from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Разрешение для проверки, что пользователь принадлежит группе 'Moderators'.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name="Moderators").exists()
