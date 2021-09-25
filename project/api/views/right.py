from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import Right
from ..serializers import RightListSerializer, RightSerializer
from . import TagMixin


class RightViewSet(ReadOnlyModelViewSet, TagMixin):
    queryset = Right.objects.order_by('-id')
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return RightListSerializer
        return RightSerializer
