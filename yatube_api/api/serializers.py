from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post


User = get_user_model()


class AuthorMixin(serializers.ModelSerializer):
    """Базовый миксин с полем Author наследуемый от ModelSerializer."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(AuthorMixin):

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('pub_date',)


class CommentSerializer(AuthorMixin):

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        exclude = ('id',)
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def validate_following(self, value):
        """Проверяет, что пользователь не подписывается сам на себя."""
        if self.context.get('request').user != value:
            return value
        raise serializers.ValidationError(
            'Ошибка - Вы не можете быть подписаны на себя.'
        )
