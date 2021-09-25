from rest_framework import serializers

from ..models import Video
from .base import BaseSerializer


class VideoSerializer(BaseSerializer):
    image = serializers.ImageField(
        max_length=None,
        allow_empty_file=False,
        use_url=False,
        required=False,
    )

    class Meta(BaseSerializer.Meta):
        model = Video
