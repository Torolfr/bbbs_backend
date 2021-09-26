from django_filters import CharFilter, FilterSet


class BookTypeFilter(FilterSet):
    types = CharFilter(field_name='type__slug', method='filter_types')

    def filter_types(self, queryset, slug, types):
        return queryset.filter(type__slug__in=(types.split(',')))


class TagFilter(FilterSet):
    tags = CharFilter(field_name='tags__slug', method='filter_tags')

    def filter_tags(self, queryset, slug, tags):
        return queryset.filter(
            tags__slug__in=tags.split(',')
        ).distinct()
