import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User

# Считаю использование\импортирование модели User из posts.models -
# целесообразным для -данного- проекта: У нас используется один пользователь,
# стандартный и импортируется всегда из одного места; при изменении модели или
# применении customUser - все что необходимо - указать данные в settings.py
# после чего - get_user_model из posts.models возьмет новую модель при инициа-
# лизации и она изменится во всех местах единовременно.
# С бОльшей вероятностью, при добавлении новых приложений и расширении проекта
# в цепочке между settings-framework-db-app что-то может пойти "не так".
# Руководствуюсь, в основном, указанием Андрея Квичанского из ревью конца 4-го
# спринта(он указал как исправление и что нужно делать импорт модели)
# А также - своим (пока малым), но имеющимся опытом борьбы с импортами и
# непереданными в нужные места переменными (импорт работал, обычно, у меня)


class Base64ImageField(serializers.ImageField):
    """Поле для обработки изображений, закодированных в формате Base64.

    Это поле позволяет принимать данные изображения в виде строки Base64,
    декодировать их и сохранять как файл изображения.

    Методы:
        to_internal_value(image_data):
            Преобразует строку Base64 в объект ContentFile и передает его
            в стандартный метод to_internal_value родительского класса.
    """

    def to_internal_value(self, img_str):
        if isinstance(img_str, str) and img_str.startswith('data:image'):
            format, imgstr = img_str.split(';base64,')
            ext = format.split('/')[-1]
            img_str = ContentFile(
                base64.b64decode(imgstr),
                name=f'temp.{ext}'
            )
        return super().to_internal_value(img_str)


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
