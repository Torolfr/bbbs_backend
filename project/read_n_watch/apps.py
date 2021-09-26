from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ReadnWatchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'read_n_watch'
    verbose_name = _(' Читать и смотреть')
