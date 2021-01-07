from django.conf import settings
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from rest_auth.models import TokenModel
from rest_auth.app_settings import TokenSerializer, create_token

from .serializers import RegistrationSerializer, LoginSerializer

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


class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = TokenModel

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        user_serializer = self.get_serializer(data=request.data, context={'request': request})
        user_serializer.is_valid(raise_exception=True)

        user = user_serializer.validated_data['user']
        token = create_token(self.token_model, user, user_serializer)
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            login(request, user)

        token_serializer = TokenSerializer(instance=token, context={'request': request})
        return Response(token_serializer.data, status=status.HTTP_200_OK)


class TokenHealthCheckAPIView(APIView):
    permission_classes = IsAuthenticated,
    contents = None

    def get(self, request):
        self.contents = {'status': 'active token'}
        return Response(self.contents)
