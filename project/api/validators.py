from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
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


def year_validator(value):
    if value > now().year:
        raise ValidationError(
            '%(value)s год больше текущего',
            code='invalid',
            params={'value': value},
        )


def image_extension_validator(value):
    return FileExtensionValidator(
        allowed_extensions=settings.IMAGE_EXTENSIONS)(value)


def file_size_validator(value):
    limit = settings.MAX_IMAGE_UPLOAD_SIZE
    if value.size > limit:
        raise ValidationError(
            _('Файл не должен быть больше '
              f'{settings.MAX_IMAGE_UPLOAD_SIZE_MB}М.')
        )
