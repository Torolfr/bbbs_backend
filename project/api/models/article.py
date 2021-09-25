from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from ..validators import file_size_validator, image_extension_validator
from .mixins import ImageFromUrlMixin


class Article(models.Model, ImageFromUrlMixin):
    title = models.CharField(
        verbose_name=_('Заголовок'),
        max_length=200,
    )
    info = models.CharField(
        verbose_name=_('Информация'),
        max_length=200,
    )
    annotation = models.TextField(
        verbose_name=_('Аннотация'),
        max_length=1024,
    )
    article_url = models.URLField(
        verbose_name=_('Ссылка на статью'),
        max_length=192,
    )
    image = ResizedImageField(
        verbose_name=_('Изображение'),
        upload_to='articles/',
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
        blank=True,
        null=True,
        help_text=_(
            'Альтернативный способ загрузки изображения. Приоритет у файла.'
        ),
    )
    output_to_main = models.BooleanField(
        verbose_name=_('Отображать на главной странице'),
        default=False,
        help_text=_(
            'Статьи с этой меткой будут отображаться на главной странице.'
        ),
    )
    pinned_full_size = models.BooleanField(
        verbose_name=_('Закрепить'),
        default=False,
        help_text=_(
            'Статья с этой меткой будет отображаться'
            'в полноразмерном формате вверху страницы.'
        ),
    )

    class Meta:
        app_label = 'api'
        ordering = ('id',)
        verbose_name = _('Статья')
        verbose_name_plural = _('Статьи')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs) -> None:
        if self.image_url and not self.image:
            self.load_image(image_url=self.image_url)
        if self.pinned_full_size:
            self.__class__.objects.filter(
                pinned_full_size=True
            ).update(
                pinned_full_size=False
            )
        return super().save(*args, **kwargs)
