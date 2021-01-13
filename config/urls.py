from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include

from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.authentication.api.views import UserViewSet


router = DefaultRouter()
router.register(r'', viewset=UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'api/users/', include(router.urls)),
    path(r'api/auth/', include('apps.authentication.api.urls')),
    path(r'api/introduction/', include('apps.introduction.api.urls')),
    path(r'api/musics/', include('apps.song.api.urls')),
    path(r'api-auth/', include('rest_framework.urls')),
]
