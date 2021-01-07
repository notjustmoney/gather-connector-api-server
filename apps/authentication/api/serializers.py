from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, exceptions

from ..models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'display_name', 'phone_number',
                  'department', 'task', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_email(self, email, password):
        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        username = None

        user = None

        try:
            username = User.objects.get(email__iexact=email).get_username()
        except User.DoesNotExist:
            pass

        if username:
            user = self.authenticate(username=username, password=password)

        if user:
            if not user.is_active:
                msg = _('비활성화된 계정입니다.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('제공된 인증자격으로 로그인 할 수 없습니다.')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    answers = serializers.HyperlinkedRelatedField(many=True, view_name='answer-detail', read_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'display_name', 'image_url', 'phone_number',
                  'department', 'task', 'is_active', 'answers']
