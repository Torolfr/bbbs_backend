import os

import requests
from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from .fields import ColorField
from .validators import file_size_validator, image_extension_validator


class ImageFromUrlMixin:
    def load_image(self, *, image_url, save=False):
        new_id = str(now().timestamp())
        directory = self.__class__.image.field.upload_to
        try:
            response = requests.get(image_url)
            if not os.path.isdir(settings.MEDIA_ROOT / f'{directory}'):
                os.mkdir(settings.MEDIA_ROOT / f'{directory}')
            with open(
                settings.MEDIA_ROOT / f'{directory}/{new_id}_pic.jpg',
                'wb'
            ) as image:
                image.write(response.content)
                self.image = f'{directory}/{new_id}_pic.jpg'
            if save:
                self.save()
        except requests.exceptions.ConnectionError:
            pass


class ActivityType(models.Model):
    name = models.CharField(
        verbose_name=_('Вид активности'),
        max_length=30,
        unique=True,
    )

    class Meta:
        verbose_name = _('Тип отдыха')
        verbose_name_plural = _('Типы отдыха')

    def __str__(self):
        return self.name


class BookType(models.Model):
    name = models.CharField(
        verbose_name=_('Название'),
        unique=True,
        max_length=128
    )
    color = ColorField(
        verbose_name=_('Цвет'),
        default='#FF0000'
    )
    slug = models.SlugField(
        verbose_name=_('Слаг (Ссылка)'),
        unique=True
    )

    class Meta:
        ordering = ('name', )
        verbose_name = _('Тип книг')
        verbose_name_plural = _('Типы книг')

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(
        verbose_name=_('Название региона'),
        max_length=128,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = _('Регион')
        verbose_name_plural = _('Регионы')

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(
        verbose_name=_('Название города'),
        max_length=128,
        unique=True,
    )
    region = models.ForeignKey(
        Region,
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
        ordering = ('-is_primary', 'name')
        verbose_name = _('Город')
        verbose_name_plural = _('Города')

    def __str__(self):
        return self.name


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
        verbose_name = _('Изображение')
        verbose_name_plural = _('Изображения')

    def __str__(self):
        try:
            return (f'{self.image_caption[:15]}.. '
                    f'({self.image.width}x{self.image.height})')
        except FileNotFoundError:
            return f'{self.image_caption} (файл не найден)'


class Tag(models.Model):
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=50,
    )
    category = models.CharField(
        verbose_name=_('Категория'),
        max_length=50,
        choices=(
            ('Фильмы', _('Фильмы')),
            ('Куда пойти', _('Куда пойти')),
            ('Вопросы', _('Вопросы')),
            ('Права', _('Права')),
            ('Видеоролики', _('Видеоролики')),
            ('Календарь', _('Календарь')),
        ),
    )
    slug = models.SlugField(
        verbose_name=_('Слаг (Ссылка)'),
        unique=True,
    )
    order = models.PositiveSmallIntegerField(
        verbose_name=_('Порядок вывода'),
        default=0,
        help_text=_(
            'Теги с меньшим значением выводятся первыми.'
        ),
    )

    class Meta:
        ordering = ('category', 'order')
        verbose_name = _('Тег')
        verbose_name_plural = _('Теги')

    def __str__(self):
        return f'{self.category}: {self.name}'
