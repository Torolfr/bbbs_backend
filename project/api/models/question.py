from django.db import models
from django.utils.translation import gettext_lazy as _


class Question(models.Model):
    title = models.TextField(
        verbose_name=_('Вопрос'),
        max_length=500,
    )
    answer = models.TextField(
        max_length=2048,
        verbose_name=_('Ответ'),
        blank=True,
        null=True,
    )
    output_to_main = models.BooleanField(
        verbose_name=_('Отображать на главной странице'),
        default=False,
        help_text=_(
            'Вопросы с этой меткой будут отображаться на главной странице.'
        ),
    )
    tags = models.ManyToManyField(
        'api.Tag',
        verbose_name=_('Тег(и)'),
        related_name='questions',
        limit_choices_to={'category': 'Вопросы'},
    )

    class Meta:
        app_label = 'api'
        ordering = ('id',)
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')

    def __str__(self):
        return self.title
