from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import CharField, TextField
from django.forms import Textarea, TextInput
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from martor.models import MartorField
from martor.widgets import AdminMartorWidget

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


@admin.register(models.Article)
class ArticleAdmin(ImageTagField, MixinAdmin):
    list_display = ('id', 'title', 'image_tag',
                    'pinned_full_size', 'output_to_main')
    search_fields = ('title', 'info', 'annotation')
    list_filter = ('pinned_full_size', 'output_to_main')


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


@admin.register(models.Movie)
class MovieAdmin(ImageTagField, MixinAdmin):
    form = forms.MovieForm
    list_display = ('id', 'title', 'link', 'image_tag', 'output_to_main')
    search_fields = ('title', 'info', 'annotation')
    list_filter = ('output_to_main', 'tags')


@admin.register(models.Video)
class VideoAdmin(ImageTagField, MixinAdmin):
    list_display = ('id', 'title', 'link', 'duration', 'resource_group',
                    'pinned_full_size', 'output_to_main', 'image_tag')
    search_fields = ('title', 'info')
    list_filter = ('resource_group', 'pinned_full_size',
                   'output_to_main', 'tags')
