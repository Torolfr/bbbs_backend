from django.conf import settings
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Count, Exists, F, OuterRef, Value
from django.db.models.functions import Concat
from django.utils.timezone import now
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response

from .filters import PlaceFilter
from .models import History, Place, Question, Right
from .serializers import (HistoryListSerializer, HistorySerializer,
                          MainSerializer, PlaceListSerializer,
                          PlaceSerializer, QuestionSerializer,
                          RightListSerializer, RightSerializer,
                          SearchResultSerializer)
from afisha.models import Event
from common.views import GetListPostPutMixin, TagMixin
from read_n_watch.models import Article, Book, Video, Movie


class HistoryViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return HistoryListSerializer
        return HistorySerializer

    def get_queryset(self):
        pair = Concat(F('mentor__first_name'), Value(' и '), F('child'))
        return History.objects.annotate(pair=pair).order_by('-id')


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


class PlacesViewSet(GetListPostPutMixin, TagMixin):
    queryset = Place.objects.exclude(moderation_flag=False).order_by('-id')
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_class = PlaceFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return PlaceListSerializer
        return PlaceSerializer

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if user.is_authenticated:
            return queryset.filter(city=user.city)
        city = self.request.GET.get('city')
        if city is not None:
            return queryset.filter(city=city)
        return queryset

    def perform_create(self, serializer):
        age = self.request.data.get('age')
        if 7 < int(age) < 11:
            age_restriction = '8-10'
        elif 10 < int(age) < 14:
            age_restriction = '11-13'
        elif 13 < int(age) < 18:
            age_restriction = '14-17'
        else:
            age_restriction = '18'
        serializer.save(
            chosen=self.request.user.is_mentor,
            age_restriction=age_restriction,
        )

    @action(methods=['get'], detail=False)
    def first(self, request):
        return Response(
            self.serializer_class(
                self.get_queryset().order_by(
                    '-chosen',
                    '-id',
                ).first()
            ).data
        )


class QuestionViewSet(GetListPostPutMixin, TagMixin):
    queryset = Question.objects.exclude(answer=None).order_by('-id')
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination


class RightViewSet(ReadOnlyModelViewSet, TagMixin):
    queryset = Right.objects.order_by('-id')
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return RightListSerializer
        return RightSerializer


MODEL_URL_MAP = {
    Article: 'articles',
    Book: 'books',
    Event: 'afisha',
    Movie: 'movies',
    Place: 'places',
    Question: 'questions',
    Right: 'rights',
    Video: 'video',
}


def build_select_dict(model):
    return {
        'model_name': f'\'{model._meta.verbose_name_plural}\'',
        'page': f'\'{MODEL_URL_MAP.get(model)}\'',
    }


def build_queryset(queryset, search_text):
    return queryset.annotate(
        rank=TrigramSimilarity('title', search_text)
    ).filter(
        rank__gt=0.071428575
    ).extra(
        select=build_select_dict(queryset.model)
    ).values('title', 'model_name', 'rank', 'page', 'id')


class SearchView(GenericViewSet, ListModelMixin):
    serializer_class = SearchResultSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        city_filter = {'city': self.request.GET.get('city')}
        resource_filter = {}
        if user.is_authenticated:
            city_filter['city'] = user.city
        else:
            resource_filter['resource_group'] = False
        SEARCH_QUERYSETS = [ # noqa N806
            Article.objects.all(),
            Event.objects.filter(
                **city_filter,
                end_at__gt=now(),
                canceled=False,
                id__isnull=not user.is_authenticated
            ),
            Place.objects.filter(moderation_flag=True, **city_filter),
            Book.objects.all(),
            Movie.objects.all(),
            Video.objects.filter(**resource_filter),
            Right.objects.all(),
            Question.objects.exclude(answer=None)
        ]
        search_text = self.request.GET.get('text')
        queryset = Article.objects.none().extra(
            select={
                'model_name': 'null',
                'rank': 'null',
                'url': 'null'
            }
        ).values('title', 'model_name', 'rank', 'url')
        for query in SEARCH_QUERYSETS:
            queryset = queryset.union(
                build_queryset(
                    query,
                    search_text
                )
            )
        return queryset.order_by('-rank')
