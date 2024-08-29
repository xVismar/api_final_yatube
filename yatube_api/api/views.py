from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from api.permissions import IsAuthor, GetPermissions
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
    permission_classes = (IsAuthor,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Переопределение метода perform_create для PostViewSet.

        Определяет автора публикации как автора запроса.
        """
        serializer.save(author=self.request.user)


class CommentViewSet(GetPermissions):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthor,)

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

        Определяет пользователя как автора запроса.
        """
        serializer.save(user=self.request.user)

    # Изначально был использован django-filter и search_field, однако,
    # платформа Практикум выдавала ошибку (старая версия filter/django) и
    # НЕ пропускала для сдачи. Пришлось заменить на ручной усложненный метод.
    # Временное решение. Вот так должно быть -
    #
    # from rest_framework.filters import SearchFilter
    # ...
    # class FollowViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    #    serializer_class = FollowSerializer
    #    permission_classes = (IsAuthenticated,)
    #    filter_backends = (DjangoFilterBackend, SearchFilter)
    #    search_fields = ('=following__username',)
    #
    #    def perform_create(self, serializer):
    #        serializer.save(user=self.request.user)
    #
    #    def perform_create(self, serializer):
    #        serializer.save(user=self.request.user)

    def post(self):
        """Переопределяем метод post для FollowViewSet.

        Создаем объект модели Follow, после прохождения сериалайзера.
        """
        return self.perform_create(FollowSerializer)

    def get(self, request):
        """Переопределяем метод get для FollowViewSet.

        Получаем список публикаций подписанного автора.
        """
        return self.list(request)

    def get_queryset(self):
        """Переопределяет метод get_queryset для FollowViewSet.

        Добавляет к queryset параметры ?search , если таковые были переданы
        И вызывает функцию поиска по данным параметрам (если отсутвуют=None).
        """
        queryset = self.request.user.follower.all()
        search_params = self.request.query_params.get('search')
        return self.custom_search(queryset, search_params)

    def custom_search(self, queryset, search_params=None):
        """Выполняет проверку, если был передан запрос с параметром ?search.

        Если параметры отсутствуют - возвращает неизмененный queryset.
        """
        if search_params:
            return queryset.filter(
                Q(following__username__icontains=search_params)
            )
        return queryset
