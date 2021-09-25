from rest_framework import serializers

from ..models import Book
from .booktype import BookTypeSerializer


class BookSerializer(serializers.ModelSerializer):
    type = BookTypeSerializer(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'
