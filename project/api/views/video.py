from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..filters import VideoFilter
from ..models import Video
from ..serializers import VideoSerializer
from . import TagMixin


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
