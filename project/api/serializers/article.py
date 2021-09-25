from rest_framework import serializers

from ..models import Article
from .base import BaseSerializer


class ArticleSerializer(BaseSerializer):
    image = serializers.ImageField(
        max_length=None,
        allow_empty_file=False,
        use_url=False,
        required=False,
    )

    class Meta(BaseSerializer.Meta):
        tags = None
        model = Article
        exclude = ['image_url']
