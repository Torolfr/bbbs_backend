from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import ActivityType, BookType, City, Image, Region, Tag


class MixinAdmin(admin.ModelAdmin):
    empty_value_display = _('-пусто-')


@admin.register(ActivityType)
class ActivityAdmin(MixinAdmin):
    list_display = ('id', 'name', )
    search_fields = ('name', )


@admin.register(BookType)
class BookTypeAdmin(MixinAdmin):
    list_display = ('id', 'name', 'slug', 'color')
    search_fields = ('name', 'slug', 'color')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Region)
class RegionAdmin(MixinAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', )


@admin.register(City)
class CityAdmin(MixinAdmin):
    list_display = ('id', 'name', 'region', 'is_primary')
    search_fields = ('name', )
    list_filter = ('region', 'is_primary')
    autocomplete_fields = ('region', )


@admin.register(Image)
class ImageAdmin(MixinAdmin):
    list_display = ('id', 'image_caption')
    search_fields = ('image_caption', )


@admin.register(Tag)
class TagAdmin(MixinAdmin):
    list_display = ('id', 'name', 'category', 'slug', 'order')
    list_editable = ('category', 'order')
    search_fields = ('name', 'category', 'slug')
    list_filter = ('category', )
    prepopulated_fields = {'slug': ('name',)}
