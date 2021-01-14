from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm, UserChangeForm

from phonenumber_field.modelfields import PhoneNumberField

from .constants.department import *
from .models import User


class UserCreationForm(UserCreationForm):
    name = forms.CharField(required=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    department = forms.ChoiceField(required=True, choices=DEPARTMENT_CHOICES)
    task = forms.CharField()

    class Meta:
        model = User
        fields = 'name', 'phone_number', 'department', 'task',
        field_classes = {'username': forms.EmailField}

    def save(self, commit=True):
        user = super(UserCreationForm, self).save()
        user.name = self.cleaned_data['name']
        user.phone_number = self.cleaned_data['phone_number']
        user.department = self.cleaned_data['department']
        user.task = self.cleaned_data['task']

        if commit:
            user.save()
        return user


class UserChangeForm(UserChangeForm):
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    department = forms.ChoiceField(required=True, choices=DEPARTMENT_CHOICES)

    class Meta:
        model = User
        exclude = 'password',
