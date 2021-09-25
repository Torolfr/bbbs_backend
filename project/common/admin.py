from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Image


class MixinAdmin(admin.ModelAdmin):
    empty_value_display = _('-пусто-')


@admin.register(Image)
class ImageAdmin(MixinAdmin):
    list_display = ('id', 'image_caption')
    search_fields = ('image_caption', )
