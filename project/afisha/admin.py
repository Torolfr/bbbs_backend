from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import EventMailing


class MixinAdmin(admin.ModelAdmin):
    empty_value_display = _('-пусто-')


@admin.register(EventMailing)
class EventMailingAdmin(MixinAdmin):
    list_display = ('id', 'event', 'user', 'get_date_sending', 'mailing_type')
    search_fields = ('event', 'user')
    list_filter = ('mailing_type', )

    @admin.display(description=_('Время отправки'))
    def get_date_sending(self, obj):
        return obj.date_sending.strftime('%d.%m.%Y %H:%M:%S')
