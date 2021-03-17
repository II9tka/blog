from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers

from backend.article.documents import ArticleDocument
from backend.utils.vesaliteimagefield_for_elasticsearch import ElasticSearchVersatileImageFieldSerializer


class ArticleListDocumentSerializer(DocumentSerializer):
    id_str = serializers.CharField(source='id')
    cover = ElasticSearchVersatileImageFieldSerializer(
        read_only=True,
        sizes=[
            ('medium_square_crop', 'crop__800x800'),
        ]
    )
    lifetime_str = serializers.CharField(source='lifetime')

    class Meta:
        document = ArticleDocument
        fields = (
            'id',
            'id_str',
            'title',
            'cover',
            'short_description',
            'created_at',
            'updated_at',
            'creator',
            'lifetime',
            'lifetime_str',
            'is_published',
            'tags',
        )
