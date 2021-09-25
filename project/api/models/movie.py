import urllib

import requests
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from ..validators import file_size_validator, image_extension_validator
from .mixins import ImageFromUrlMixin


def get_image_url_from_link(video_url: str) -> str:
    '''для получения url независимо от вида ссылки на видео youtube'''
    try:
        response = requests.get(video_url)
        desired_url = response.url
        parsed_url = urllib.parse.urlparse(desired_url)
        parameters = urllib.parse.parse_qs(parsed_url.query)
        video_id = parameters['v'][0]
        return f'https://img.youtube.com/vi/{video_id}/0.jpg'
    except requests.exceptions.ConnectionError:
        raise ConnectionError


class Movie(models.Model, ImageFromUrlMixin):
    title = models.CharField(
        verbose_name=_('Заголовок'),
        max_length=128,
    )
    info = models.CharField(
        verbose_name=_('Информация'),
        max_length=512,
    )
    annotation = models.TextField(
        verbose_name=_('Аннотация'),
        max_length=1024,
    )
    image = ResizedImageField(
        verbose_name=_('Изображение'),
        upload_to='movies/',
        blank=True,
        null=True,
        size=[1280, 720],
        crop=['middle', 'center'],
        help_text=settings.IMAGE_FIELD_HELP_TEXT,
        validators=[file_size_validator, image_extension_validator],
    )
    link = models.URLField(
        verbose_name=_('Ссылка на фильм'),
        max_length=192,
    )
    output_to_main = models.BooleanField(
        verbose_name=_('Отображать на главной странице'),
        default=False,
        help_text=_(
            'Фильмы с этой меткой будут отображаться на главной странице.'
        ),
    )
    tags = models.ManyToManyField(
        'api.Tag',
        verbose_name=_('Теги'),
        related_name='movies',
        limit_choices_to={'category': 'Фильмы'},
    )

    class Meta:
        app_label = 'api'
        ordering = ('id',)
        verbose_name = _('Фильм')
        verbose_name_plural = _('Фильмы')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs) -> None:
        if self.link and not self.image:
            try:
                video_thumbnail_url = get_image_url_from_link(self.link)
                self.load_image(image_url=video_thumbnail_url)
            except ConnectionError:
                super().save(*args, **kwargs)
        return super().save(*args, **kwargs)
