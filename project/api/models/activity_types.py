from django.db import models
from django.utils.translation import gettext_lazy as _


class ActivityType(models.Model):
    name = models.CharField(
        verbose_name=_('Вид активности'),
        max_length=30,
        unique=True,
    )

    class Meta:
        app_label = 'api'
        ordering = ('id',)
        verbose_name = _('Тип отдыха')
        verbose_name_plural = _('Типы отдыха')

    def __str__(self):
        return self.name
