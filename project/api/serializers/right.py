from rest_framework import serializers

from ..models import Right
from .tag import TagSerializer


class RightListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Right
        fields = ['id', 'title', 'tags']


class RightNextSerializer(RightListSerializer):
    class Meta:
        model = Right
        fields = ['id', 'title']


class RightSerializer(RightListSerializer):
    next_article = serializers.SerializerMethodField()

    class Meta:
        model = Right
        fields = '__all__'

    def get_next_article(self, obj):
        queryset = Right.objects.filter(id__lt=obj.id)
        tags = self.context['request'].query_params.get('tags')
        if tags is not None and len(tags) > 0:
            queryset = queryset.filter(tags__slug__in=tags.split(','))
        if not queryset.exists():
            return None
        serializer = RightNextSerializer(queryset.first())
        return serializer.data
