from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import City, Region


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name=_('Адрес электронной почты'),
        blank=False,
    )
    city = models.ForeignKey(
        City,
        verbose_name=_('Город'),
        related_name='users',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text=_(
            'Обязательное поле для наставника.'
        )
    )
    region = models.ForeignKey(
        Region,
        verbose_name=_('Регион'),
        related_name='users',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text=_(
            'Обязательное поле для регионального модератора.'
        )
    )
    is_mentor = models.BooleanField(
        verbose_name=_('Наставник'),
        default=False,
        help_text=_(
            'Выберите эту метку, если пользователь является наставником.'
        )
    )
    curator = models.ForeignKey(
        'CustomUser',
        verbose_name=_('Куратор'),
        related_name='mentors',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text=_(
            'Обязательное поле для наставника.'
        )
    )

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name[:1]}.'
        return self.username

    def clean(self):
        errors = {}
        if self.is_mentor:
            if self.curator is None:
                errors['curator'] = ValidationError(
                    _('У наставника должен быть куратор'))
            if self.city is None:
                errors['city'] = ValidationError(
                    _('У наставника должен быть город'))
        if self.curator:
            if not self.is_mentor:
                errors['curator'] = ValidationError(
                    _('Куратор может быть только у наставника'))
            if self.curator == self:
                errors['curator'] = ValidationError(
                    _('Нельзя быть куратором для самого себя'))
        if errors:
            raise ValidationError(errors)
