from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from backend.article.documents import ArticleDocument
from backend.utils.vesaliteimagefield_for_elasticsearch import ElasticSearchVersatileImageFieldSerializer


class ArticleListDocumentSerializer(DocumentSerializer):
    cover = ElasticSearchVersatileImageFieldSerializer(
        read_only=True,
        sizes=[
            ('medium_square_crop', 'crop__800x800'),
        ]
    )

    class Meta:
        document = ArticleDocument
        fields = (
            'id',
            'cs',
            'id_str',
            'title',
            'cover',
            'description',
            'short_description',
            'created_at',
            'updated_at',
            'creator',
        )
