from rest_framework import serializers

from .models import Article, Book, Catalog, Movie, Video
from common.serializers import BookTypeSerializer, TagSerializer


class BaseSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False, read_only=True)

    class Meta:
        exclude = ['output_to_main', ]


class ArticleSerializer(BaseSerializer):
    image = serializers.ImageField(
        max_length=None,
        allow_empty_file=False,
        use_url=False,
        required=False,
    )

    class Meta(BaseSerializer.Meta):
        tags = None
        model = Article
        exclude = ['image_url']


class BookSerializer(serializers.ModelSerializer):
    type = BookTypeSerializer(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'


class CatalogNextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ['id', 'title']


class CatalogSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None,
        allow_empty_file=False,
        use_url=False,
        required=False,
    )
    next_article = serializers.SerializerMethodField()

    class Meta:
        model = Catalog
        exclude = ['image_url']

    def get_next_article(self, obj):
        queryset = Catalog.objects.filter(id__lt=obj.id)
        if not queryset.exists():
            return None
        serializer = CatalogNextSerializer(queryset.first())
        return serializer.data


class CatalogListSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None,
        allow_empty_file=False,
        use_url=False,
        required=False,
    )

    class Meta:
        model = Catalog
        exclude = ['description', 'image_url', 'body']


class MovieSerializer(BaseSerializer):
    image = serializers.ImageField(
        max_length=None,
        allow_empty_file=False,
        use_url=False,
        required=False,
    )

    class Meta(BaseSerializer.Meta):
        model = Movie


class VideoSerializer(BaseSerializer):
    image = serializers.ImageField(
        max_length=None,
        allow_empty_file=False,
        use_url=False,
        required=False,
    )

    class Meta(BaseSerializer.Meta):
        model = Video
