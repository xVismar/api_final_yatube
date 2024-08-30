from api.permissions import IsAuthor
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions


class GetPermissions(ModelViewSet):
    """Переопределяет метод получения разрешений, наследует от ModelViewSet."""

    permission_classes = (IsAuthor,)

    def get_permissions(self):
        return (
            super().get_permissions()
            if self.action not in {'list', 'retrieve'}
            else (permissions.AllowAny(),)
        )
