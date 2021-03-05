from rest_framework import serializers

from taggit_serializer.serializers import (
    TagListSerializerField,
    TaggitSerializer
)
from versatileimagefield.serializers import VersatileImageFieldSerializer

from backend.api.v1.filer.serializers import UploadImageSerializer, UploadRelatedImageSerializer
from backend.article.models import Article, ArticleImage
from backend.utils.serializers import get_obj_or_raise_error


class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    id_str = serializers.CharField(source='id', read_only=True)
    creator = serializers.CharField(source='creator.username', read_only=True)
    cover = VersatileImageFieldSerializer(
        source='get_cover',
        read_only=True,
        sizes=[
            ('medium_square_crop', 'crop__800x800'),
        ]
    )
    title = serializers.CharField(read_only=True)
    short_description = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    lifetime = serializers.IntegerField(read_only=True)
    lifetime_str = serializers.CharField(source='lifetime', read_only=True)
    tags = TagListSerializerField(read_only=True)

    class Meta:
        fields = (
            'id',
            'creator',
            'title',
            'short_description',
            'lifetime',
            'created_at',
            'updated_at',
        )


class ArticleImageSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        source='get_image',
        read_only=True,
        sizes=[
            ('full_size', 'url'),
            ('medium_square_crop', 'crop__400x400'),
        ]
    )

    class Meta:
        model = ArticleImage
        exclude = ('article',)


class ArticleModelSerializer(TaggitSerializer, serializers.ModelSerializer):
    id_str = serializers.CharField(source='id', read_only=True)
    cover = VersatileImageFieldSerializer(
        source='get_cover',
        read_only=True,
        sizes=[
            ('full_size', 'url'),
            ('medium_square_crop', 'crop__800x800'),
        ]
    )
    creator = serializers.CharField(source='creator.username', read_only=True)
    tags = TagListSerializerField()
    images = ArticleImageSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = '__all__'


class UploadArticleCoverSerializer(UploadImageSerializer):
    def get_setattr_obj_name(self) -> str:
        return 'article'


class UploadArticleImageSerializer(UploadRelatedImageSerializer):
    image = serializers.ImageField(write_only=True)

    def create(self, validated_data):
        get_obj_or_raise_error(
            model=Article, pk_args='article_pk', context=self.context, validated_data=validated_data
        )
        return super().create(validated_data)

    def get_setattr_obj_name(self) -> str:
        return 'image'

    class Meta:
        model = ArticleImage
        fields = ('id', 'image',)

# class ArticleCommentsSerializer(serializers.Serializer):
