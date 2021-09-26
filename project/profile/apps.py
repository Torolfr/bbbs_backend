from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profile'
    verbose_name = _(' Личный кабинет')
