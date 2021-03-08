from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from backend.article.documents import ArticleDocument
from ..article.serializers import ArticleListModelSerializer


class ArticleListDocumentSerializer(DocumentSerializer, ArticleListModelSerializer):
    class Meta:
        document = ArticleDocument
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
