from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CommentViewSet, GroupViewSet, PostViewSet

app_name = 'api_v1'

router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('groups', GroupViewSet, basename='group')
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comment_post'
)

urlpatterns = [
    path('/', include(router.urls)),
    path('/', include('djoser.urls')),
    path('/', include('djoser.urls.jwt'))
]
