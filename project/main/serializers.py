from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import History, HistoryImage, Place, Question, Right
from afisha.serializers import EventSerializer
from common.serializers import BaseSerializer, TagSerializer
from read_n_watch.serializers import (
    ArticleSerializer,
    MovieSerializer,
    VideoSerializer,
)

User = get_user_model()


class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['first_name', 'email']
        model = User


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


class PlaceSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False, read_only=True)
    image = serializers.ImageField(
        max_length=None,
        allow_empty_file=False,
        use_url=False,
        required=False,
    )

    class Meta:
        model = Place
        exclude = [
            'image_url',
            'age_restriction',
            'output_to_main',
            'moderation_flag',
        ]

    def validate_age(self, value):
        if value > 25:
            raise serializers.ValidationError(
                _('Слишком большой возраст для ребёнка')
            )
        elif value < 8:
            raise serializers.ValidationError(
                _('Возраст не может быть меньше 8')
            )
        return value


class PlaceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        exclude = [
            'tags',
            'city',
            'image',
            'image_url',
            'age_restriction',
            'output_to_main',
            'moderation_flag',
        ]


class QuestionSerializer(BaseSerializer):
    answer = serializers.CharField(read_only=True)

    class Meta(BaseSerializer.Meta):
        model = Question


class MainSerializer(serializers.Serializer):
    event = EventSerializer(required=False, read_only=True)
    history = HistorySerializer(required=False, read_only=True)
    place = PlaceSerializer(required=False, read_only=True)
    articles = ArticleSerializer(many=True, required=False, read_only=True)
    movies = MovieSerializer(many=True, required=False, read_only=True)
    video = VideoSerializer(required=False, read_only=True)
    questions = QuestionSerializer(many=True, required=False, read_only=True)


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


class SearchResultSerializer(serializers.Serializer):
    title = serializers.CharField()
    model_name = serializers.CharField()
    page = serializers.CharField()
    id = serializers.CharField()
