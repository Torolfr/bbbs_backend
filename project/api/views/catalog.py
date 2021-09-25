from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import Catalog
from ..serializers import CatalogListSerializer, CatalogSerializer


class CatalogView(ReadOnlyModelViewSet):
    queryset = Catalog.objects.order_by('-id')
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return CatalogListSerializer
        return CatalogSerializer
