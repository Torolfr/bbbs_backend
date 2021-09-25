from django_filters import CharFilter, FilterSet, NumberFilter
from django_filters.filters import BooleanFilter

from .models import Event, Place, Video


class PlaceFilter(FilterSet):
    min_age = NumberFilter(field_name='age', lookup_expr='gte')
    max_age = NumberFilter(field_name='age', lookup_expr='lte')
    tags = CharFilter(field_name='tags__slug', method='filter_tags')
    chosen = BooleanFilter(field_name='chosen')
    age_restriction = CharFilter(
        field_name='age_restriction',
        method='filter_age_restriction',
    )

    def filter_age_restriction(self, queryset, slug, age_restriction):
        return queryset.filter(
            age_restriction__in=age_restriction.split(',')
        ).distinct()

    def filter_tags(self, queryset, slug, tags):
        return queryset.filter(
            tags__slug__in=tags.split(',')
        ).distinct()

    class Meta:
        model = Place
        fields = ['age', 'tags', 'chosen', 'age_restriction']


class EventFilter(FilterSet):
    months = CharFilter(field_name='start_at', method='filter_months')
    years = CharFilter(field_name='start_at', method='filter_years')

    def filter_months(self, queryset, slug, months):
        return queryset.filter(start_at__month__in=months.split(','))

    def filter_years(self, queryset, slug, years):
        return queryset.filter(start_at__year__in=years.split(','))

    class Meta:
        model = Event
        fields = ['months', 'years']


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
