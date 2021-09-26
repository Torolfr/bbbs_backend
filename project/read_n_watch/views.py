from django.db.models.expressions import F, Window
from django.db.models.functions import Rank
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import VideoFilter
from .models import Article, Book, Catalog, Movie, Video
from .serializers import (
    ArticleSerializer,
    BookSerializer,
    CatalogListSerializer,
    CatalogSerializer,
    MovieSerializer,
    VideoSerializer,
)
from common.filters import BookTypeFilter
from common.views import TagMixin
from common.models import BookType
from common.serializers import BookTypeSerializer


class ArticleViewSet(ReadOnlyModelViewSet):
    queryset = Article.objects.all().order_by('-pinned_full_size', '-id')
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination


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
    filter_class = BookTypeFilter

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


class CatalogView(ReadOnlyModelViewSet):
    queryset = Catalog.objects.order_by('-id')
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return CatalogListSerializer
        return CatalogSerializer


class MovieView(ReadOnlyModelViewSet, TagMixin):
    queryset = Movie.objects.order_by('-id')
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination


class VideoView(ReadOnlyModelViewSet, TagMixin):
    serializer_class = VideoSerializer
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination
    filter_class = VideoFilter

    def get_queryset(self):
        exclude_keys = {}
        if not self.request.user.is_authenticated:
            exclude_keys['resource_group'] = True
        return Video.objects.exclude(
            **exclude_keys
        ).order_by('-pinned_full_size', '-id')
