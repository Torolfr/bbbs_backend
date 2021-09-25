from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from .validators import file_size_validator, image_extension_validator


class Image(models.Model):
    image = ResizedImageField(
        upload_to='images/',
        verbose_name=_('Изображение'),
        size=[1280, 720],
        crop=['middle', 'center'],
        help_text=settings.IMAGE_FIELD_HELP_TEXT,
        validators=[file_size_validator, image_extension_validator],
    )
    image_caption = models.CharField(
        verbose_name=_('Подпись к изображению'),
        max_length=200,
    )

    class Meta:
        app_label = 'common'
        verbose_name = _('Изображение')
        verbose_name_plural = _('Изображения')

    def __str__(self):
        try:
            return (f'{self.image_caption[:15]}.. '
                    f'({self.image.width}x{self.image.height})')
        except FileNotFoundError:
            return f'{self.image_caption} (файл не найден)'
