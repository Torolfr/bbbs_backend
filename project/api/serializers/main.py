from rest_framework.serializers import Serializer

from ..serializers import (
    ArticleSerializer,
    EventSerializer,
    HistorySerializer,
    MovieSerializer,
    PlaceSerializer,
    QuestionSerializer,
    VideoSerializer,
)


class MainSerializer(Serializer):
    event = EventSerializer(required=False, read_only=True)
    history = HistorySerializer(required=False, read_only=True)
    place = PlaceSerializer(required=False, read_only=True)
    articles = ArticleSerializer(many=True, required=False, read_only=True)
    movies = MovieSerializer(many=True, required=False, read_only=True)
    video = VideoSerializer(required=False, read_only=True)
    questions = QuestionSerializer(many=True, required=False, read_only=True)
