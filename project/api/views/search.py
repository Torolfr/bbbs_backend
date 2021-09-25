from django.contrib.postgres.search import TrigramSimilarity
from django.utils.timezone import now
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from ..models import Article, Book, Event, Movie, Place, Question, Right, Video
from ..serializers import SearchResultSerializer

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
