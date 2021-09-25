from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import CharField, TextField
from django.forms import Textarea, TextInput
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _
from martor.models import MartorField
from martor.widgets import AdminMartorWidget
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from . import forms, models

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
        MartorField: {'widget': AdminMartorWidget},
    }


@admin.register(models.ActivityType)
class ActivityAdmin(MixinAdmin):
    list_display = ('id', 'name', )
    search_fields = ('name', )


@admin.register(models.Article)
class ArticleAdmin(ImageTagField, MixinAdmin):
    list_display = ('id', 'title', 'image_tag',
                    'pinned_full_size', 'output_to_main')
    search_fields = ('title', 'info', 'annotation')
    list_filter = ('pinned_full_size', 'output_to_main')


@admin.register(models.BookType)
class BookTypeAdmin(MixinAdmin):
    list_display = ('id', 'name', 'slug', 'color')
    search_fields = ('name', 'slug', 'color')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Book)
class BookAdmin(MixinAdmin):
    list_display = ('id', 'title', 'author', 'year', 'type', 'get_color')
    list_filter = ('type', )
    search_fields = ('title', 'author', 'annotation')

    @admin.display(description=_('Цвет'))
    def get_color(self, obj):
        try:
            color = obj.type.color
        except AttributeError:
            color = None
        return color # noqa R504
    get_color.admin_order_field = 'color'


@admin.register(models.Catalog)
class CatalogAdmin(ImageTagField, MixinAdmin):
    list_display = ('id', 'title', 'image_tag')
    search_fields = ('title', )


@admin.register(models.City)
class CityAdmin(MixinAdmin):
    list_display = ('id', 'name', 'region', 'is_primary')
    search_fields = ('name', )
    list_filter = ('region', 'is_primary')
    autocomplete_fields = ('region', )


@admin.register(models.Diary)
class DiaryAdmin(ImageTagField, MixinAdmin):
    list_display = ('id', 'mentor', 'place', 'date',
                    'mark', 'sent_to_curator', 'image_tag')
    search_fields = ('place', 'description')
    list_filter = ('mark', )


@admin.register(models.Event)
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
        if request.user.has_perm('api.events_in_all_cities'):
            return queryset
        return queryset.filter(city__in=request.user.region.cities.all())

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user
        if (db_field.name == 'city'
                and not user.has_perm('api.events_in_all_cities')):
            kwargs['queryset'] = models.City.objects.filter(region=user.region)
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


class HistoryImageInline(admin.TabularInline):
    model = models.HistoryImage
    min_num = 4
    extra = 0


@admin.register(models.History)
class HistoryAdmin(ImageTagField, MixinAdmin):
    list_display = ('id', 'title', 'mentor', 'child',
                    'output_to_main', 'image_tag')
    search_fields = ('title', 'description')
    list_filter = ('output_to_main', )
    inlines = [HistoryImageInline]


@admin.register(models.Movie)
class MovieAdmin(ImageTagField, MixinAdmin):
    form = forms.MovieForm
    list_display = ('id', 'title', 'link', 'image_tag', 'output_to_main')
    search_fields = ('title', 'info', 'annotation')
    list_filter = ('output_to_main', 'tags')


@admin.register(models.Question)
class QuestionAdmin(MixinAdmin):
    list_display = ('id', 'get_title', 'get_answer')
    search_fields = ('title', 'answer')
    list_filter = ('output_to_main', 'tags')

    @admin.display(description=_('Вопрос'))
    def get_title(self, obj):
        title = obj.title
        if title is not None:
            return f'{title[:50]}..?'
        return title

    @admin.display(description=_('Ответ'))
    def get_answer(self, obj):
        answer = obj.answer
        if answer is not None:
            return f'{answer[:50]}..'
        return answer


@admin.register(models.Place)
class PlaceAdmin(ImageTagField, MixinAdmin):
    list_display = ('id', 'title', 'city', 'activity_type', 'age_restriction',
                    'age', 'chosen', 'moderation_flag', 'output_to_main')
    list_editable = ('age_restriction', )
    search_fields = ('title', 'description')
    list_filter = ('city', 'activity_type', 'age_restriction', 'chosen',
                   'moderation_flag', 'output_to_main', 'tags')
    radio_fields = {'gender': admin.HORIZONTAL}

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.has_perm('api.places_in_all_cities'):
            return queryset
        return queryset.filter(city__in=request.user.region.cities.all())

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user
        if (db_field.name == 'city'
                and not user.has_perm('api.places_in_all_cities')):
            kwargs['queryset'] = models.City.objects.filter(region=user.region)
        return super(
            PlaceAdmin,
            self
        ).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(models.Right)
class RightAdmin(MixinAdmin):
    list_display = ('id', 'title', 'get_description')
    search_fields = ('title', 'description', 'text')
    list_filter = ('tags', )

    @admin.display(description=_('Описание'))
    def get_description(self, obj):
        description = obj.description
        if description is not None:
            return f'{description[:50]}..'
        return description


@admin.register(models.Region)
class RegionAdmin(MixinAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', )


@admin.register(models.Tag)
class TagAdmin(MixinAdmin):
    list_display = ('id', 'name', 'category', 'slug', 'order')
    list_editable = ('category', 'order')
    search_fields = ('name', 'category', 'slug')
    list_filter = ('category', )
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Video)
class VideoAdmin(ImageTagField, MixinAdmin):
    list_display = ('id', 'title', 'link', 'duration', 'resource_group',
                    'pinned_full_size', 'output_to_main', 'image_tag')
    search_fields = ('title', 'info')
    list_filter = ('resource_group', 'pinned_full_size',
                   'output_to_main', 'tags')
