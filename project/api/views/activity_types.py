from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import ActivityType
from ..serializers import ActivityTypeSerializer


class ActivityTypeView(ReadOnlyModelViewSet):
    queryset = ActivityType.objects.all()
    serializer_class = ActivityTypeSerializer
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination
