from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(
            self,
            name,
            display_name,
            email,
            phone_number,
            department,
            task,
            password=None,):

        if not name:
            raise ValueError('회원생성에는 반드시 이름이 필요합니다.')
        if not email:
            raise ValueError('회원생성에는 반드시 이메일이 필요합니다.')
        if not phone_number:
            raise ValueError('회원생성에는 반드시 전화번호가 필요합니다.')
        if not department:
            raise ValueError('회원생성에는 반드시 부서입력이 필요합니다.')
        if not task:
            raise ValueError('회원생성에는 반드시 담당업무가 필요합니다.')
        if not password:
            raise ValueError('회원생성에는 반드시 비밀번호가 필요합니다.')
        if not display_name:
            display_name = name
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            display_name=display_name,
            image_url='/static/profile/default.png',
            phone_number=phone_number,
            department=department,
            task=task
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            name,
            display_name,
            email,
            phone_number,
            department,
            task,
            password=None,):

        user = self.create_user(
            name,
            display_name,
            email,
            phone_number,
            department,
            task,
            password=password
        )
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_adminuser(
            self,
            name,
            display_name,
            email,
            phone_number,
            department,
            task,
            password=None,):

        user = self.create_user(
            name,
            display_name,
            email,
            phone_number,
            department,
            task,
            password=password,
        )
        user.is_superuser = False
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,)
    name = models.CharField(max_length=30, blank=False)
    display_name = models.CharField(
        verbose_name='display name',
        max_length=30,)
    image_url = models.CharField(
        verbose_name='image url',
        max_length=255,
        default='/static/profile/default.png',)
    phone_number = PhoneNumberField(
        verbose_name='phone number',
        unique=True)
    department = models.CharField(max_length=30)
    task = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'display_name', 'phone_number', 'department', 'task']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """특정한 권한 소유 여부"""
        return True

    def has_module_perms(self, app_label):
        """app label에 해당하는 app의 권한 소유 여부"""
        return True

    @property
    def is_staff(self):
        return self.is_admin
