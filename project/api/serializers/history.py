from rest_framework import serializers

from ..models import History, HistoryImage
from .profile import MentorSerializer


class HistoryImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='image.id')
    image = serializers.ImageField(source='image.image', use_url=False)
    image_caption = serializers.CharField(source='image.image_caption')

    class Meta:
        fields = ['id', 'image', 'image_caption']
        model = HistoryImage


class HistoryNextSerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['id', 'title']


class HistorySerializer(serializers.ModelSerializer):
    mentor = MentorSerializer()
    image = serializers.ImageField(use_url=False)
    images = HistoryImageSerializer(many=True)
    next_article = serializers.SerializerMethodField()

    class Meta:
        model = History
        exclude = ['output_to_main', 'image_url']

    def get_next_article(self, obj):
        queryset = History.objects.filter(id__lt=obj.id)
        if not queryset.exists():
            return None
        serializer = HistoryNextSerializer(queryset.first())
        return serializer.data


class HistoryListSerializer(serializers.ModelSerializer):
    pair = serializers.CharField()

    class Meta:
        model = History
        fields = ['id', 'pair']
