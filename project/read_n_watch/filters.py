from django_filters import CharFilter, FilterSet
from django_filters.filters import BooleanFilter

from .models import Video


class VideoFilter(FilterSet):
    tags = CharFilter(field_name='tags__slug', method='filter_tags')
    resource_group = BooleanFilter(field_name='resource_group')

    def filter_tags(self, queryset, slug, tags):
        return queryset.filter(
            tags__slug__in=tags.split(',')
        ).distinct()

    class Meta:
        model = Video
        fields = ['tags', 'resource_group']
