from django.db import models
from django.utils.translation import gettext_lazy as _

from ..fields import fields


class BookType(models.Model):
    name = models.CharField(
        verbose_name=_('Название'),
        unique=True,
        max_length=128
    )
    color = fields.ColorField(
        verbose_name=_('Цвет'),
        default='#FF0000'
    )
    slug = models.SlugField(
        verbose_name=_('Слаг (Ссылка)'),
        unique=True
    )

    class Meta:
        app_label = 'api'
        ordering = ('name', )
        verbose_name = _('Тип книг')
        verbose_name_plural = _('Типы книг')

    def __str__(self):
        return self.name
