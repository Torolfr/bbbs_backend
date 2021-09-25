from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class EventMailing(models.Model):
    event = models.ForeignKey(
        'api.Event',
        verbose_name=_('Событие'),
        related_name='mailings',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('Пользователь'),
        related_name='event_mailings',
        on_delete=models.CASCADE,
    )
    date_sending = models.DateTimeField(
        verbose_name=_('Время отправки'),
        auto_now_add=True,
    )
    mailing_type = models.CharField(
        verbose_name=_('Тип сообщения'),
        max_length=12,
        choices=(
            ('cancellation', _('Отмена')),
            ('reminder', _('Напоминание'))
        ),
    )

    class Meta:
        ordering = ('-date_sending',)
        verbose_name = _('Рассылка уведомлений')
        verbose_name_plural = _('Рассылки уведомлений')
