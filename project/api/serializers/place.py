from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ..models import Place
from .tag import TagSerializer


class PlaceSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False, read_only=True)
    image = serializers.ImageField(
        max_length=None,
        allow_empty_file=False,
        use_url=False,
        required=False,
    )

    class Meta:
        model = Place
        exclude = [
            'image_url',
            'age_restriction',
            'output_to_main',
            'moderation_flag',
        ]

    def validate_age(self, value):
        if value > 25:
            raise serializers.ValidationError(
                _('Слишком большой возраст для ребёнка')
            )
        elif value < 8:
            raise serializers.ValidationError(
                _('Возраст не может быть меньше 8')
            )
        return value


class PlaceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        exclude = [
            'tags',
            'city',
            'image',
            'image_url',
            'age_restriction',
            'output_to_main',
            'moderation_flag',
        ]
