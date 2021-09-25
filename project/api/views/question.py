from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Question
from ..serializers import QuestionSerializer
from . import GetListPostPutMixin, TagMixin


class QuestionViewSet(GetListPostPutMixin, TagMixin):
    queryset = Question.objects.exclude(answer=None).order_by('-id')
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination
