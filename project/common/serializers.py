from rest_framework import serializers

from .models import ActivityType, BookType, City, Tag


class ActivityTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityType
        fields = '__all__'


class BookTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookType
        fields = ('slug', 'name', 'color')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['region']
        model = City


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['category']
        model = Tag


class BaseSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False, read_only=True)

    class Meta:
        exclude = ['output_to_main', ]
