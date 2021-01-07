from django.conf import settings
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import User

from .serializers import RegistrationSerializer, UserSerializer

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)


class RegistrationAPIView(APIView):
    permission_classes = AllowAny,
    serializer_class = RegistrationSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TokenHealthCheckAPIView(APIView):
    permission_classes = IsAuthenticated,
    contents = None

    def get(self, request):
        self.contents = {'status': 'active token'}
        return Response(self.contents)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list, retrieve action
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
