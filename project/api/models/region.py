from django.db import models
from django.utils.translation import gettext_lazy as _


class Region(models.Model):
    name = models.CharField(
        verbose_name=_('Название региона'),
        max_length=128,
        unique=True,
    )

    class Meta:
        app_label = 'api'
        ordering = ('name',)
        verbose_name = _('Регион')
        verbose_name_plural = _('Регионы')

    def __str__(self):
        return self.name
