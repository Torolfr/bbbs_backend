import urllib

import requests
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from martor.models import MartorField

from .validators import (
    file_size_validator,
    image_extension_validator,
    year_validator
)
from common.models import BookType, ImageFromUrlMixin, Tag


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
        ordering = ('-id',)
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


class Book(models.Model):
    title = models.CharField(
        verbose_name=_('Заголовок'),
        max_length=128,
    )
    author = models.CharField(
        verbose_name=_('Автор'),
        max_length=256,
    )
    year = models.SmallIntegerField(
        verbose_name=_('Год публикации'),
        validators=[year_validator],
    )
    annotation = models.TextField(
        verbose_name=_('Аннотация'),
        max_length=1024,
    )
    type = models.ForeignKey(
        BookType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Тип книги'),
        related_name='books'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = _('Книга')
        verbose_name_plural = _('Книги')
        indexes = [
            models.Index(fields=['type'], name='book_type_slug_index')
        ]

    def __str__(self):
        return self.title


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
        ordering = ('-id',)
        verbose_name = _('Справочник')
        verbose_name_plural = _('Справочник')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs) -> None:
        if self.image_url and not self.image:
            self.load_image(image_url=self.image_url)
        return super().save(*args, **kwargs)


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
        Tag,
        verbose_name=_('Теги'),
        related_name='movies',
        limit_choices_to={'category': 'Фильмы'},
    )

    class Meta:
        ordering = ('-id',)
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


class Video(models.Model, ImageFromUrlMixin):
    title = models.CharField(
        verbose_name=_('Заголовок'),
        max_length=128,
    )
    info = models.TextField(
        verbose_name=_('Информация'),
        max_length=512,
    )
    image = ResizedImageField(
        verbose_name=_('Изображение'),
        upload_to='videos/',
        blank=True,
        null=True,
        size=[1280, 720],
        crop=['middle', 'center'],
        help_text=settings.IMAGE_FIELD_HELP_TEXT,
        validators=[file_size_validator, image_extension_validator],
    )
    link = models.URLField(
        verbose_name=_('Ссылка на видеоролик'),
        max_length=192,
    )
    duration = models.PositiveIntegerField(
        verbose_name=_('Длина видео в сек.'),
        validators=(MinValueValidator(1), MaxValueValidator(86400)),
    )
    output_to_main = models.BooleanField(
        verbose_name=_('Отображать на главной странице'),
        default=False,
        help_text=_(
            'Видео с этой меткой будут отображаться на главной странице.'
        ),
    )
    pinned_full_size = models.BooleanField(
        verbose_name=_('Закрепить'),
        default=False,
        help_text=_(
            'Видео с этой меткой будет отображаться'
            'в полноразмерном формате вверху страницы.'
        ),
    )
    resource_group = models.BooleanField(
        verbose_name=_('Ресурсная группа'),
        default=False,
        help_text=_(
            'Видео с этой меткой не будут показаны'
            'не авторизованным пользователям.'
        ),
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('Теги'),
        related_name='videos',
        limit_choices_to={'category': 'Видеоролики'},
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = _('Видеоролик')
        verbose_name_plural = _('Видеоролики')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs) -> None:
        if self.link and not self.image:
            try:
                video_thumbnail_url = get_image_url_from_link(self.link)
                self.load_image(image_url=video_thumbnail_url)
            except ConnectionError:
                super().save(*args, **kwargs)
        if self.pinned_full_size:
            self.__class__.objects.filter(
                pinned_full_size=True
            ).update(
                pinned_full_size=False
            )
        return super().save(*args, **kwargs)
