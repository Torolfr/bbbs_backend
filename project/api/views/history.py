from django.db.models import F, Value
from django.db.models.functions import Concat
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import History
from ..serializers import HistoryListSerializer, HistorySerializer


class HistoryViewSet(ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return HistoryListSerializer
        return HistorySerializer

    def get_queryset(self):
        pair = Concat(F('mentor__first_name'), Value(' и '), F('child'))
        return History.objects.annotate(pair=pair).order_by('-id')
