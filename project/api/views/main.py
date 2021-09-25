from django.conf import settings
from django.db.models import Count, Exists, F, OuterRef
from django.utils.timezone import now
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import Article, Event, History, Movie, Place, Question, Video
from ..serializers.main import MainSerializer


class MainPage:
    def __init__(self, event=None, history=None, place=None,
                 articles=None, movies=None, video=None, questions=None):
        self.event = event
        self.history = history
        self.place = place
        self.articles = articles
        self.movies = movies
        self.video = video
        self.questions = questions


def get_event(request):
    user = request.user
    if not user.is_authenticated:
        return None
    booked = Event.objects.filter(pk=OuterRef('pk'), participants=user)
    events = Event.objects.filter(
        end_at__gt=now(),
        city=user.city,
    ).annotate(
        booked=Exists(booked)
    ).annotate(
        remain_seats=F('seats') - Count('participants')
    )
    return events.order_by('start_at').first()


def get_place(request):
    user = request.user
    city = request.data.get('city')
    places = Place.objects.filter(
        output_to_main=True,
        moderation_flag=True
    ).order_by(
        '-id'
    )
    if user.is_authenticated:
        if places.filter(city=user.city).exists():
            return places.filter(city=user.city).first()
        return places.first()
    if city is not None:
        if places.filter(city=city).exists():
            return places.filter(city=city).first()
    return places.first()


def get_video(request):
    user = request.user
    video = Video.objects.filter(output_to_main=True).order_by('-id')
    if user.is_authenticated:
        return video.first()
    return video.filter(resource_group=False).first()


class MainViewSet(RetrieveAPIView):
    serializer_class = MainSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = MainPage()
        instance.event = get_event(request)
        instance.place = get_place(request)
        instance.video = get_video(request)
        instance.history = History.objects.filter(output_to_main=True).last()
        instance.articles = Article.objects.filter(
            output_to_main=True
        ).order_by(
            '-id'
        )[:settings.MAIN_ARTICLES_LENGTH]
        instance.movies = Movie.objects.filter(
            output_to_main=True
        ).order_by(
            '-id'
        )[:settings.MAIN_MOVIES_LENGTH]
        instance.questions = Question.objects.filter(
            output_to_main=True
        ).order_by(
            '-id'
        )[:settings.MAIN_QUESTION_LENGTH]
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
