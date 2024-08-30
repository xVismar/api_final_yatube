from django.shortcuts import get_object_or_404
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from api.mixins import GetPermissions
from api.serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer
)
from posts.models import Group, Post


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(GetPermissions):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Переопределение метода perform_create для PostViewSet.

        Определяет автора публикации как автора запроса.
        """
        serializer.save(author=self.request.user)


class CommentViewSet(GetPermissions):
    serializer_class = CommentSerializer

    def get_post(self):
        """Получаем публикацию или 404 (pk передан через URL)."""
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        """Получаем все связанные с объектом комментарии."""
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """Переопределение метода perform_create для CommentViewSet.

        Определяет автора комментария как автора запроса и добавляет
        объект публицаии.
        """
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('=following__username',)

    def perform_create(self, serializer):
        """Переопределение метода perform_create для FollowViewSet.

        Определяет автора запроса как пользователь.
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Переопределение метода get_queryset для FollowViewSet.

        Возвращает список постов пользователя.
        """
        return self.request.user.follower
