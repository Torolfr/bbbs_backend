from rest_framework import serializers

from ..models import Movie
from .base import BaseSerializer


class MovieSerializer(BaseSerializer):
    image = serializers.ImageField(
        max_length=None,
        allow_empty_file=False,
        use_url=False,
        required=False,
    )

    class Meta(BaseSerializer.Meta):
        model = Movie
