from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import CharField, TextField
from django.forms import Textarea, TextInput
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from martor.models import MartorField
from martor.widgets import AdminMartorWidget

from .models import History, HistoryImage, Place, Question, Right
from common.models import City

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


class HistoryImageInline(admin.TabularInline):
    model = HistoryImage
    min_num = 3
    extra = 0


@admin.register(History)
class HistoryAdmin(ImageTagField, MixinAdmin):
    list_display = ('id', 'title', 'mentor', 'child',
                    'output_to_main', 'image_tag')
    search_fields = ('title', 'description')
    list_filter = ('output_to_main', )
    inlines = [HistoryImageInline]


@admin.register(Question)
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


@admin.register(Place)
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
        if request.user.has_perm('main.places_in_all_cities'):
            return queryset
        return queryset.filter(city__in=request.user.region.cities.all())

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user
        if (db_field.name == 'city'
                and not user.has_perm('main.places_in_all_cities')):
            kwargs['queryset'] = City.objects.filter(region=user.region)
        return super(
            PlaceAdmin,
            self
        ).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Right)
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
