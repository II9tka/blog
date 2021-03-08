from rest_framework import serializers, validators

from taggit_serializer.serializers import (
    TagListSerializerField,
    TaggitSerializer
)
from versatileimagefield.serializers import VersatileImageFieldSerializer
from backend.api.v1.filer.serializers import (
    UploadImageSerializer,
    UploadRelatedImageSerializer,
)

from backend.account.models import Account
from backend.article.models import (
    Article,
    ArticleImage,
    ArticleComment,
    ArticleCommentLike,
)

from backend.utils.serializers import (
    get_obj_or_raise_error,
    RecursiveChildrenSerializer,
)


class CommentCreatorSerializer(serializers.ModelSerializer):
    account_url = serializers.HyperlinkedIdentityField(
        view_name='account-detail',
        read_only=True
    )

    class Meta:
        model = Account
        fields = ('id', 'first_name', 'last_name', 'account_url',)


class BaseArticleModelSerializer(serializers.ModelSerializer):
    id_str = serializers.CharField(source='id', read_only=True)
    creator = serializers.CharField(source='creator.username', read_only=True)


class ArticleCommentLikeModelSerializer(BaseArticleModelSerializer):
    def run_validators(self, value):
        for validator in self.validators:
            if isinstance(validator, validators.UniqueTogetherValidator):
                self.validators.remove(validator)
        super().run_validators(value)

    def create(self, validated_data):
        get_obj_or_raise_error(
            model=ArticleComment, pk_args='comment_pk', context=self.context, validated_data=validated_data
        )
        model = self.Meta.model
        instance, is_created = model.objects.get_or_create(**validated_data)
        if not is_created:
            instance.delete()
        return instance

    class Meta:
        model = ArticleCommentLike
        exclude = ('comment',)


class ArticleCommentModelSerializer(BaseArticleModelSerializer):
    is_liked = serializers.SerializerMethodField()
    creator = CommentCreatorSerializer(read_only=True)
    children = RecursiveChildrenSerializer(many=True, read_only=True)

    def _get_user(self):
        return self.context['request'].user

    def get_is_liked(self, instance):
        return instance.likes.all().filter(creator=self._get_user()).exists()

    def create(self, validated_data):
        get_obj_or_raise_error(
            model=Article, pk_args='article_pk', context=self.context, validated_data=validated_data
        )
        return super().create(validated_data)

    class Meta:
        model = ArticleComment
        fields = (
            'id',
            'id_str',
            'creator',
            'text',
            'created_at',
            'is_liked',
            'parent',
            'children',
        )
        extra_kwargs = {
            'parent': {'write_only': True}
        }


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


class ArticleListModelSerializer(TaggitSerializer, BaseArticleModelSerializer):
    cover = VersatileImageFieldSerializer(
        source='get_cover',
        read_only=True,
        sizes=[
            ('medium_square_crop', 'crop__800x800'),
        ]
    )
    lifetime_str = serializers.CharField(source='lifetime', read_only=True)
    tags = TagListSerializerField(read_only=True)

    class Meta:
        model = Article
        fields = (
            'id',
            'id_str',
            'title',
            'creator',
            'cover',
            'lifetime',
            'lifetime_str',
            'created_at',
            'updated_at',
            'short_description',
            'tags',
        )


class ArticleDetailModelSerializer(ArticleListModelSerializer):
    tags = TagListSerializerField(read_only=True)
    comments = ArticleCommentModelSerializer(read_only=True, many=True)
    images = ArticleImageSerializer(read_only=True, many=True)

    class Meta(ArticleListModelSerializer.Meta):
        fields = ArticleListModelSerializer.Meta.fields + (
            'description',
            'comments',
            'images',
        )


class UploadArticleCoverSerializer(UploadImageSerializer):
    def get_setattr_obj_name(self) -> str:
        return 'article'


class UploadArticleImageSerializer(UploadRelatedImageSerializer):
    image = serializers.ImageField(source='image.image')

    def get_setattr_obj_name(self) -> str:
        return 'image'

    def create(self, validated_data):
        get_obj_or_raise_error(
            model=Article, pk_args='article_pk', context=self.context, validated_data=validated_data
        )
        return super().create(validated_data)

    class Meta:
        model = ArticleImage
        exclude = ('article',)
