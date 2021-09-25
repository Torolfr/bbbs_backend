from django.db.models.expressions import F, Window
from django.db.models.functions import Rank
from django_filters.filters import CharFilter
from django_filters.filterset import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import Book, BookType
from ..serializers import BookSerializer, BookTypeSerializer


class TypeFilter(FilterSet):
    types = CharFilter(field_name='type__slug', method='filter_types')

    def filter_types(self, queryset, slug, types):
        return queryset.filter(type__slug__in=(types.split(',')))


class BookView(ReadOnlyModelViewSet):
    queryset = Book.objects.annotate(
        rank=Window(
            expression=Rank(),
            order_by=F('pk').desc(),
            partition_by=[F('type_id')]
        )
    ).order_by('rank', '-pk')
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination
    filterset_backends = [DjangoFilterBackend]
    filter_class = TypeFilter

    @action(methods=['get'], detail=False)
    def types(self, request):
        related_query_name = self.queryset.model._meta.get_field(
            'type'
        ).related_query_name()
        filter_key = f'{related_query_name}__in'
        types = BookType.objects.filter(
            **{filter_key: self.queryset}
        ).distinct()
        serializer = BookTypeSerializer(types, many=True)
        return Response(serializer.data)
