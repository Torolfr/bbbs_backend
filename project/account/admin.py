from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .forms import CustomAdminPasswordChangeForm, CustomUserCreationForm

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    change_password_form = CustomAdminPasswordChangeForm
    empty_value_display = _('-пусто-')
    list_display = ('id', 'username', 'email', 'first_name', 'last_name',
                    'city', 'region', 'is_staff', 'is_mentor', 'get_curator')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('city', 'region', 'is_mentor',
                   'is_staff', 'is_active', 'is_superuser')
    autocomplete_fields = ('city', 'region', 'curator')
    readonly_fields = ('date_joined', 'last_login')

    add_fieldsets = (
        (_('Логин/пароль'), {
            'fields': ('username', )
        }),
        (_('Персональная информация'), {
            'fields': (('first_name', 'last_name'), 'email',
                       ('city', 'region'), 'is_mentor', 'curator')
        }),
        (_('Права доступа'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups'),
        }),
        (_('Даты последнего входа/регистрации'), {
            'fields': ('last_login', 'date_joined')
        }),
    )

    fieldsets = (
        (_('Логин/пароль'), {
            'fields': ('username', 'password')
        }),
        (_('Персональная информация'), {
            'fields': (('first_name', 'last_name'), 'email',
                       ('city', 'region'), 'is_mentor', 'curator')
        }),
        (_('Права доступа'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups'),
        }),
        (_('Даты последнего входа/регистрации'), {
            'fields': ('last_login', 'date_joined')
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()
        if not is_superuser:
            disabled_fields |= {
                'is_superuser',
                'user_permissions',
            }
        if (
            not is_superuser
            and obj is not None
            and (obj.is_superuser or obj == request.user)
        ):
            disabled_fields |= {
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }
        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
        return form

    @admin.display(description=_('Куратор'))
    def get_curator(self, obj):
        curator = obj.curator
        if curator:
            url = (
                reverse('admin:account_customuser_changelist')
                + f'{curator.id}/change/'
            )
            curator = f'{curator.first_name} {curator.last_name[:1]}'
            return format_html('<a href="{}">{}</a>', url, curator)
        return None
