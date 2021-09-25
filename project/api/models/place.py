from django.conf import settings
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from ..validators import file_size_validator, image_extension_validator
from .mixins import ImageFromUrlMixin


class Place(models.Model, ImageFromUrlMixin):
    title = models.CharField(
        verbose_name=_('Название'),
        max_length=200,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_('Комментарий'),
    )
    image = ResizedImageField(
        verbose_name=_('Изображение'),
        upload_to='places/',
        blank=True,
        null=True,
        size=[1280, 720],
        crop=['middle', 'center'],
        help_text=settings.IMAGE_FIELD_HELP_TEXT,
        validators=[file_size_validator, image_extension_validator],
    )
    image_url = models.URLField(
        verbose_name=_('Ссылка на изображение'),
        blank=True,
        null=True,
        help_text=_(
            'Альтернативный способ загрузки изображения. Приоритет у файла.'
        ),
    )
    link = models.URLField(
        verbose_name=_('Сайт'),
        blank=True,
        null=True,
    )
    city = models.ForeignKey(
        'api.City',
        verbose_name=_('Город'),
        related_name='places',
        on_delete=models.CASCADE,
    )
    address = models.CharField(
        verbose_name=_('Адрес'),
        max_length=200,
    )
    activity_type = models.ForeignKey(
        blank=True,
        to='api.ActivityType',
        verbose_name=_('Вид активности'),
        related_name='places',
        on_delete=models.PROTECT,
    )
    gender = models.CharField(
        blank=True,
        verbose_name=_('Пол ребёнка'),
        max_length=6,
        choices=(('male', _('Мальчик')), ('female', _('Девочка'))),
    )
    age = models.SmallIntegerField(
        blank=True,
        verbose_name=_('Возраст ребёнка'),
        validators=[
            validators.MinValueValidator(8),
            validators.MaxValueValidator(25),
        ],
    )
    age_restriction = models.CharField(
        verbose_name=_('Целевой возраст'),
        max_length=50,
        choices=(
            ('8-10', '8-10'),
            ('11-13', '11-13'),
            ('14-17', '14-17'),
            ('18', '18+'),
            ('any', _('Любой'))
        ),
    )
    chosen = models.BooleanField(
        verbose_name=_('Выбор наставника'),
        default=False,
    )
    output_to_main = models.BooleanField(
        verbose_name=_('Отображать на главной странице'),
        default=False,
        help_text=_(
            'Места с этой меткой будут отображаться на главной странице сайта.'
        ),
    )
    moderation_flag = models.BooleanField(
        verbose_name=_('Отметка о модерации'),
        default=False,
        help_text=_(
            'Места без этой метки не будут отображаться на сайте.'
        ),
    )
    tags = models.ManyToManyField(
        to='api.Tag',
        verbose_name=_('Тег(и)'),
        related_name='places',
        limit_choices_to={'category': 'Куда пойти'},
    )

    class Meta:
        app_label = 'api'
        ordering = ('-id',)
        verbose_name = _('Куда пойти')
        verbose_name_plural = _('Куда пойти')
        permissions = (
            ('places_in_all_cities', _('Можно смотреть места всех городов')),
        )
        indexes = [
            models.Index(fields=['moderation_flag', 'city'])
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs) -> None:
        if self.image_url and not self.image:
            self.load_image(image_url=self.image_url)
        return super().save(*args, **kwargs)
