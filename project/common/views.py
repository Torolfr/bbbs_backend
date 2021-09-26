from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from .filters import TagFilter
from .models import ActivityType, City, Tag
from .serializers import ActivityTypeSerializer, CitySerializer, TagSerializer


class GetListPostPutMixin(
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin
):
    pass


class ActivityTypeView(ReadOnlyModelViewSet):
    queryset = ActivityType.objects.all()
    serializer_class = ActivityTypeSerializer
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination


class CityViewSet(ReadOnlyModelViewSet):
    queryset = City.objects.all().order_by('-is_primary', 'name')
    serializer_class = CitySerializer
    permission_classes = [AllowAny]
    pagination_class = None


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.order_by('order')
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None


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
