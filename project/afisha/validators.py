from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


def event_lifetime_validator(event):
    if event.end_at <= now():
        raise ValidationError(
            _('Событие "%(event)s" уже закончилось'),
            code='invalid',
            params={'event': event},
        )


def free_seats_validator(event):
    if event.participants.count() >= event.seats:
        raise ValidationError(
            _('Все места на "%(event)s" уже заняты'),
            code='invalid',
            params={'event': event},
        )


def event_canceled_validator(event):
    if event.canceled:
        raise ValidationError(
            _('Событие "%(event)s" отменено, запись невозможна'),
            code='invalid',
            params={'event': event},
        )
