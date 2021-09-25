from rest_framework import serializers

from ..models import BookType


class BookTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookType
        fields = ('slug', 'name', 'color')
