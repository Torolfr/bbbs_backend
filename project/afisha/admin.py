from django.contrib import admin
from django.db.models import CharField, TextField
from django.forms import Textarea, TextInput
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from .models import Event, EventMailing
from common.models import City


class MixinAdmin(admin.ModelAdmin):
    empty_value_display = _('-пусто-')
    ordering = ('-id',)
    formfield_overrides = {
        CharField: {'widget': TextInput(attrs={'size': 80})},
        TextField: {'widget': Textarea(attrs={'rows': 8, 'cols': 80})},
    }


@admin.register(Event)
class EventAdmin(MixinAdmin):
    list_display = ('id', 'title', 'get_start_at',
                    'get_end_at', 'city', 'taken_seats', 'seats')
    list_filter = ('city', 'tags', 'canceled')
    search_fields = ('title', 'contact', 'address', 'description')
    formfield_overrides = {
        PhoneNumberField: {'widget': PhoneNumberInternationalFallbackWidget},
    }

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.has_perm('afisha.events_in_all_cities'):
            return queryset
        return queryset.filter(city__in=request.user.region.cities.all())

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user
        if (db_field.name == 'city'
                and not user.has_perm('afisha.events_in_all_cities')):
            kwargs['queryset'] = City.objects.filter(region=user.region)
        return super(
            EventAdmin,
            self
        ).formfield_for_foreignkey(db_field, request, **kwargs)

    def taken_seats(self, obj):
        count = obj.participants.count()
        url = (
            reverse('admin:account_customuser_changelist')
            + '?'
            + urlencode({'events__id': f'{obj.id}'})
        )
        return format_html('<a href="{}">{} чел.</a>', url, count)

    taken_seats.short_description = 'Кол-во участников'

    @admin.display(description=_('Время начала'))
    def get_start_at(self, obj):
        return obj.start_at.strftime('%d.%m.%Y %H:%M')

    @admin.display(description=_('Время окончания'))
    def get_end_at(self, obj):
        return obj.end_at.strftime('%d.%m.%Y %H:%M')


@admin.register(EventMailing)
class EventMailingAdmin(MixinAdmin):
    list_display = ('id', 'event', 'user', 'get_date_sending', 'mailing_type')
    search_fields = ('event', 'user')
    list_filter = ('mailing_type', )

    @admin.display(description=_('Время отправки'))
    def get_date_sending(self, obj):
        return obj.date_sending.strftime('%d.%m.%Y %H:%M:%S')
