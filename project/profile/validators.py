from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _


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
