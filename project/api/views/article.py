from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import Article
from ..serializers import ArticleSerializer


class ArticleViewSet(ReadOnlyModelViewSet):
    queryset = Article.objects.all().order_by('-pinned_full_size', '-id')
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination
