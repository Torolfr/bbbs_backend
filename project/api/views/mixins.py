from django_filters import CharFilter, FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..models import Tag
from ..serializers import TagSerializer


class GetListPostPutMixin(
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin
):
    pass


class TagFilter(FilterSet):
    tags = CharFilter(field_name='tags__slug', method='filter_tags')

    def filter_tags(self, queryset, slug, tags):
        return queryset.filter(
            tags__slug__in=tags.split(',')
        ).distinct()


class TagMixin:
    filterset_backends = [DjangoFilterBackend]
    filter_class = TagFilter

    @action(methods=['get'], detail=False)
    def tags(self, request):
        related_query_name = self.get_queryset().model._meta.get_field(
            'tags'
        ).related_query_name()
        filter_key = f'{related_query_name}__isnull'
        tags = Tag.objects.filter(**{filter_key: False}).distinct()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
