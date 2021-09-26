from django_filters import CharFilter, FilterSet

from .models import Event


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
