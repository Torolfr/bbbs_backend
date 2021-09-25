from rest_framework import serializers

from .tag import TagSerializer


class BaseSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False, read_only=True)

    class Meta:
        exclude = ['output_to_main', ]
