from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from martor.models import MartorField

from ..validators import file_size_validator, image_extension_validator
from .mixins import ImageFromUrlMixin


class Catalog(models.Model, ImageFromUrlMixin):
    title = models.CharField(
        verbose_name=_('Заголовок'),
        max_length=128,
    )
    description = models.TextField(
        verbose_name=_('Верхний абзац'),
        max_length=1024,
        help_text=_(
            'Отображается над изображением.'
        ),
    )
    image = ResizedImageField(
        upload_to='catalog/',
        verbose_name=_('Изображение'),
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
    image_caption = models.CharField(
        verbose_name=_('Подпись к изображению'),
        max_length=200,
        blank=True,
        null=True,
        help_text=_(
            'Отображается под изображением.'
        ),
    )
    body = MartorField(
        verbose_name=_('Текст статьи'),
        help_text=_(
            'Основной текст статьи. Пожалуйста, используйте форматирование.'
        ),
    )

    class Meta:
        app_label = 'api'
        ordering = ('-id',)
        verbose_name = _('Справочник')
        verbose_name_plural = _('Справочник')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs) -> None:
        if self.image_url and not self.image:
            self.load_image(image_url=self.image_url)
        return super().save(*args, **kwargs)
