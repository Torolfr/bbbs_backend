from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import CharField, TextField
from django.forms import Textarea, TextInput
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Diary, DiaryMailing

User = get_user_model()


class ImageTagField(admin.ModelAdmin):
    readonly_fields = ('image_tag',)

    def image_tag(self, instance):
        if instance.image:
            return format_html(
                '<img src="{0}" style="max-height: 50px"/>',
                instance.image.url
            )
        return None


class MixinAdmin(admin.ModelAdmin):
    empty_value_display = _('-пусто-')
    ordering = ('-id',)
    formfield_overrides = {
        CharField: {'widget': TextInput(attrs={'size': 80})},
        TextField: {'widget': Textarea(attrs={'rows': 8, 'cols': 80})},
    }


@admin.register(Diary)
class DiaryAdmin(ImageTagField, MixinAdmin):
    list_display = ('id', 'mentor', 'place', 'date',
                    'mark', 'sent_to_curator', 'image_tag')
    search_fields = ('place', 'description')
    list_filter = ('mark', )


@admin.register(DiaryMailing)
class EventMailingAdmin(MixinAdmin):
    list_display = ('id', 'diary', 'mentor', 'email', 'get_date_sending')
    search_fields = ('diary', 'mentor', 'email')

    @admin.display(description=_('Время отправки'))
    def get_date_sending(self, obj):
        return obj.date_sending.strftime('%d.%m.%Y %H:%M:%S')
