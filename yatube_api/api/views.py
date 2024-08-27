from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import (
    GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
)

from api.permissions import IsAuthor, ReadOnly
from api.serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer
)
from posts.models import Group, Post


class PermissionsMixin(ModelViewSet):
    permission_classes = (IsAuthor,)

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'list':
            return (ReadOnly(),)
        return super().get_permissions()


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(PermissionsMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(PermissionsMixin):
    serializer_class = CommentSerializer

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = FollowSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    permission_classes = (IsAuthenticated,)
    search_fields = ('=following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
