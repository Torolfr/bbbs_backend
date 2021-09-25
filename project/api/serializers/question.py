from rest_framework import serializers

from ..models import Question
from .base import BaseSerializer


class QuestionSerializer(BaseSerializer):
    answer = serializers.CharField(read_only=True)

    class Meta(BaseSerializer.Meta):
        model = Question
