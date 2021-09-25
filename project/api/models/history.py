from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from martor.models import MartorField

from ..validators import file_size_validator, image_extension_validator
from .mixins import ImageFromUrlMixin

User = get_user_model()


class History(models.Model, ImageFromUrlMixin):
    title = models.CharField(
        verbose_name=_('Заголовок'),
        max_length=200,
    )
    mentor = models.ForeignKey(
        User,
        verbose_name=_('Наставник'),
        on_delete=models.CASCADE,
    )
    child = models.CharField(
        verbose_name=_('Имя ребёнка'),
        max_length=100,
    )
    together_since = models.DateField(
        verbose_name=_('Вместе с'),
    )
    image = ResizedImageField(
        verbose_name=_('Изображение'),
        upload_to='history/',
        blank=True,
        null=True,
        size=[1280, 720],
        crop=['middle', 'center'],
        help_text=settings.IMAGE_FIELD_HELP_TEXT,
        validators=[file_size_validator, image_extension_validator],
    )
    image_url = models.URLField(
        verbose_name=_('Ссылка на изображение'),
        max_length=192,
        help_text=_(
            'Альтернативный способ загрузки изображения. Приоритет у файла.'
        ),
    )
    description = models.TextField(
        verbose_name=_('Верхний абзац'),
        max_length=1024,
        help_text=_(
            'Отображается над основным текстом статьи.'
        ),
    )
    uper_body = MartorField(
        verbose_name=_('Текст статьи над слайдером'),
        help_text=_(
            'Текст статьи над слайдером с изображениями. '
            'Для выделения абзаца используйте блок Quote (Ctrl + Q).'
        ),
    )
    lower_body = MartorField(
        verbose_name=_('Текст статьи под слайдером'),
        help_text=_(
            'Текст статьи под слайдером с изображениями. '
        ),
    )
    output_to_main = models.BooleanField(
        verbose_name=_('Отображать на главной странице'),
        default=False,
        help_text=_(
            'Истории с этой меткой будут отображаться на главной странице.'
        ),
    )

    class Meta:
        app_label = 'api'
        ordering = ('-id',)
        verbose_name = _('История')
        verbose_name_plural = _('Истории')
        constraints = [
            models.UniqueConstraint(
                fields=['mentor', 'child'],
                name='mentor_and_child_uniq_together'),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs) -> None:
        if self.image_url and not self.image:
            self.load_image(image_url=self.image_url)
        return super().save(*args, **kwargs)


class HistoryImage(models.Model):
    history = models.ForeignKey(
        History,
        verbose_name=_('История'),
        related_name='images',
        on_delete=models.CASCADE,
    )
    image = models.ForeignKey(
        'common.Image',
        verbose_name=_('Изображение'),
        related_name='histories',
        on_delete=models.PROTECT,
    )
    order = models.PositiveSmallIntegerField(
        verbose_name=_('Порядок вывода'),
        default=0,
    )

    class Meta:
        app_label = 'api'
        ordering = ('order',)
        verbose_name = _('Изображение в слайдере')
        verbose_name_plural = _('Изображения в слайдере')
