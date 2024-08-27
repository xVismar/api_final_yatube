from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from api.views import FollowViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1', include('api.urls', namespace='api_v1')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path(
        'api/v1/follow/',
        FollowViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='follow'
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
