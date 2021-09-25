from django.db import models
from django.utils.translation import gettext_lazy as _


class City(models.Model):
    name = models.CharField(
        verbose_name=_('Название города'),
        max_length=128,
        unique=True,
    )
    region = models.ForeignKey(
        'api.Region',
        verbose_name=_('Регион'),
        related_name='cities',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    is_primary = models.BooleanField(
        verbose_name=_('Приоритет вывода'),
        default=False,
        help_text=_(
            'Города с этой меткой будут отображаться в начале списка.'
        ),
    )

    class Meta:
        app_label = 'api'
        ordering = ('-is_primary', 'name')
        verbose_name = _('Город')
        verbose_name_plural = _('Города')

    def __str__(self):
        return self.name
