from django.db import models
from django.utils.translation import gettext_lazy as _
from martor.models import MartorField

from .mixins import ImageFromUrlMixin


class Right(models.Model, ImageFromUrlMixin):
    title = models.CharField(
        verbose_name=_('Заголовок'),
        max_length=200,
    )
    description = models.TextField(
        verbose_name=_('Верхний абзац'),
        max_length=1024,
        help_text=_(
            'Отображается над основным текстом статьи.'
        ),
    )
    body = MartorField(
        verbose_name=_('Текст статьи'),
        help_text=_(
            'Основной текст статьи. '
            'Для покраски абзаца используйте блок Quote (Ctrl + Q).'
        ),
    )
    tags = models.ManyToManyField(
        'api.Tag',
        verbose_name=_('Тег(и)'),
        related_name='rights',
        limit_choices_to={'category': 'Права'},
    )

    class Meta:
        app_label = 'api'
        ordering = ('-id',)
        verbose_name = _('Право')
        verbose_name_plural = _('Права')

    def __str__(self):
        return self.title
