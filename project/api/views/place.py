from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from ..filters import PlaceFilter
from ..models import Place
from ..serializers import PlaceListSerializer, PlaceSerializer
from .mixins import GetListPostPutMixin, TagMixin


class PlacesViewSet(GetListPostPutMixin, TagMixin):
    queryset = Place.objects.exclude(moderation_flag=False).order_by('-id')
    serializer_class = PlaceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
