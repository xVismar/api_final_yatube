"""Модуль содержит классы разрешений для API проекта Yatube."""
from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """Проверка аутентификации и авторства поста/комментария."""

    message = 'Изменение чужого контента запрещено!'

    def has_permission(self, request, view):
        """Проверяет, аутентифицирован ли пользователь.

        В случае анонимного пользователя - возвращает "только для чтения".
        """
        return (
            request.user.is_authenticated
            if request.method not in permissions.SAFE_METHODS
            else True
        )

    def has_object_permission(self, request, view, post):
        """Проверяет, является ли пользователь автором поста/комментария."""
        return post.author == request.user
