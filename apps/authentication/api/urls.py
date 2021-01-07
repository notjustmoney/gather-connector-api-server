from django.conf.urls import url
from django.urls import path, include

from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    LoginView,
    RegistrationAPIView,
    TokenHealthCheckAPIView
)

urlpatterns = [
    path(r'', include('rest_auth.urls')),
    # url(r'^login/?$', LoginView.as_view()),
    url(r'^registration/?$', RegistrationAPIView.as_view()),
    url(r'^token-healthcheck/?$', TokenHealthCheckAPIView.as_view()),
]
