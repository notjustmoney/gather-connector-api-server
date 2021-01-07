from django.conf.urls import url
from django.urls import path, include

from .views import (
    RegistrationAPIView,
    TokenHealthCheckAPIView
)

urlpatterns = [
    path(r'', include('rest_auth.urls')),
    url(r'^registration/?$', RegistrationAPIView.as_view()),
    url(r'^token-healthcheck/?$', TokenHealthCheckAPIView.as_view()),
]
