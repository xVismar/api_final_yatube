"""Модуль содержит классы разрешений для API проекта Yatube."""
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet


class ReadOnly(permissions.BasePermission):
    """Разрешения для просмотра для незарегистрированных пользователей."""

    def has_permission(self, request, view):
        """Переопределяет метод, проверка если запрос == GET, HEAD, OPTIONS."""
        return request.method in permissions.SAFE_METHODS


class IsAuthor(ReadOnly):
    """Проверка аутентификации и авторства поста/комментария."""

    message = 'Изменение чужого контента запрещено!'

    def has_permission(self, request, view):
        """Проверяет, аутентифицирован ли пользователь."""
        return request.user.is_authenticated

    def has_object_permission(self, request, view, post):
        """Проверяет, является ли пользователь автором поста/комментария."""
        if request.method not in permissions.SAFE_METHODS:
            return post.author == request.user


class GetPermissions(ModelViewSet):
    """Переопределяет метод получения разрешений, наследует от ModelViewSet."""

    def get_permissions(self):
        """Предоставления доступа 'только для чтения'."""
        if self.action in {'retrieve', 'list'}:
            return (ReadOnly(),)
        return super().get_permissions()
