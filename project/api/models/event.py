from django.contrib.auth import get_user_model
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Extract
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from ..validators import (event_canceled_validator, # noqa I001
                          event_lifetime_validator, free_seats_validator) # noqa I001
# noqa I005
User = get_user_model()


class Event(models.Model):
    city = models.ForeignKey(
        'api.City',
        verbose_name=_('Город мероприятия'),
        related_name='events',
        on_delete=models.PROTECT,
    )
    address = models.CharField(
        verbose_name=_('Адрес мероприятия'),
        max_length=200,
    )
    contact = models.CharField(
        verbose_name=_('Контактное лицо'),
        max_length=200,
    )
    phone_number = PhoneNumberField(
        verbose_name=_('Контактный телефон'),
    )
    title = models.CharField(
        verbose_name=_('Заголовок'),
        max_length=200,
    )
    description = models.TextField(
        verbose_name=_('Описание мероприятия'),
        max_length=1000,
    )
    start_at = models.DateTimeField(
        verbose_name=_('Время начала'),
    )
    end_at = models.DateTimeField(
        verbose_name=_('Время окончания'),
    )
    seats = models.PositiveSmallIntegerField(
        verbose_name=_('Количество мест'),
        validators=[validators.MinValueValidator(1)],
    )
    participants = models.ManyToManyField(
        User,
        through='Participant',
        through_fields=('event', 'participant'),
        verbose_name=_('Участники'),
        related_name='events',
    )
    tags = models.ForeignKey(
        to='api.Tag',
        verbose_name=_('Тег'),
        related_name='events',
        on_delete=models.PROTECT,
        limit_choices_to={'category': 'Календарь'},
    )
    canceled = models.BooleanField(
        verbose_name=_('Отметка об отмене события'),
        default=False,
        help_text=_(
            'События с этой меткой помечаются как "Отмененные", '
            'запись на них становится недоступной.'
        )
    )

    class Meta:
        app_label = 'api'
        ordering = ('id',)
        verbose_name = _('Календарь')
        verbose_name_plural = _('Календарь')
        permissions = (
            ('events_in_all_cities', _('Можно смотреть события всех городов')),
        )
        indexes = [
            models.Index(
                Extract('start_at', 'month'),
                name='event_start_at_month_index'
            ),
            models.Index(
                Extract('start_at', 'year'),
                name='event_start_at_year_index'
            )
        ]

    def __str__(self):
        return self.title

    def clean(self):
        errors = {}
        if self.start_at > self.end_at:
            errors['end_at'] = ValidationError(
                _('Конец события не может быть раньше начала'))
        if self.end_at < now():
            errors['end_at'] = ValidationError(
                _('Конец события не может быть в прошлом'))
        if self.start_at.date() != self.end_at.date():
            errors['end_at'] = ValidationError(
                _('Время окончания события должно быть в один день с началом'))
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Participant(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        validators=[
            event_lifetime_validator,
            free_seats_validator,
            event_canceled_validator,
        ]
    )
    participant = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    class Meta:
        app_label = 'api'
        ordering = ('id',)
        verbose_name = _('Запись на событие')
        verbose_name_plural = _('Записи на события')
        constraints = [
            models.UniqueConstraint(
                fields=('event', 'participant',),
                name='event_participant_uniquetogether',
            )
        ]
