from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = 'email', 'name', 'display_name', 'phone_number', \
                   'department', 'task', 'is_active', 'is_superuser', 'is_admin',
    list_filter = 'is_superuser', 'is_admin',
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        ('Personal Info', {'fields': (
            'display_name', 'phone_number', 'department', 'task')}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
    )

    add_fieldsets = (
        ('Account Info', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
        ('Personal Info', {'fields': (
            'name', 'display_name', 'phone_number', 'department', 'task')}),
    )
    search_fields = 'email',
    ordering = 'department',
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
