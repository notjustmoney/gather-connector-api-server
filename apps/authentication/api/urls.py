from django.conf.urls import url

from .views import (
    RegistrationAPIView,
)

urlpatterns = [
    url(r'^auth/registration/?$', RegistrationAPIView.as_view()),
]