from django.shortcuts import get_object_or_404
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet


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

    def perform_create(self, serializer):
        """Переопределение метода perform_create для FollowViewSet.

        Определяет автора запроса как пользователь.
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Переопределяет метод get_queryset для FollowViewSet.

        Добавляет к queryset параметры ?search , если таковые имеются.
        """
        queryset = self.request.user.follower.all()
        search_params = self.request.query_params.get('search')
        return (
            queryset if not search_params
            else queryset.filter(following__username__icontains=search_params)
        )
