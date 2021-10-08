from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from martor.models import MartorField

from common.models import ActivityType, City, Image, ImageFromUrlMixin, Tag
from common.validators import file_size_validator, image_extension_validator

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
        blank=True,
        null=True,
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
        Image,
        verbose_name=_('Изображение'),
        related_name='histories',
        on_delete=models.PROTECT,
    )
    order = models.PositiveSmallIntegerField(
        verbose_name=_('Порядок вывода'),
        default=0,
    )

    class Meta:
        ordering = ('order',)
        verbose_name = _('Изображение в слайдере')
        verbose_name_plural = _('Изображения в слайдере')


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
        City,
        verbose_name=_('Город'),
        related_name='places',
        on_delete=models.CASCADE,
    )
    address = models.CharField(
        verbose_name=_('Адрес'),
        max_length=200,
    )
    activity_type = models.ForeignKey(
        ActivityType,
        blank=True,
        null=True,
        verbose_name=_('Вид активности'),
        related_name='places',
        on_delete=models.PROTECT,
    )
    gender = models.CharField(
        blank=True,
        null=True,
        verbose_name=_('Пол ребёнка'),
        max_length=6,
        choices=(('male', _('Мальчик')), ('female', _('Девочка'))),
    )
    age = models.SmallIntegerField(
        blank=True,
        null=True,
        verbose_name=_('Возраст ребёнка'),
        validators=[
            validators.MinValueValidator(8),
            validators.MaxValueValidator(25),
        ],
    )
    age_restriction = models.CharField(
        verbose_name=_('Целевой возраст'),
        max_length=50,
        default='any',
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
        Tag,
        verbose_name=_('Тег(и)'),
        related_name='places',
        limit_choices_to={'category': 'Куда пойти'},
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = _('Куда пойти')
        verbose_name_plural = _('Куда пойти')
        permissions = (
            ('places_in_all_cities', _('Просмотр "Куда пойти" всех городов')),
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
        Tag,
        verbose_name=_('Тег(и)'),
        related_name='questions',
        limit_choices_to={'category': 'Вопросы'},
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')

    def __str__(self):
        return self.title


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
        Tag,
        verbose_name=_('Тег(и)'),
        related_name='rights',
        limit_choices_to={'category': 'Права'},
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = _('Право')
        verbose_name_plural = _('Права')

    def __str__(self):
        return self.title
