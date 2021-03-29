from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    CompoundSearchFilterBackend, MultiMatchSearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet

from backend.article.documents import ArticleDocument
from .serializers import ArticleListDocumentSerializer


class ArticleSearchViewSet(BaseDocumentViewSet):
    document = ArticleDocument
    serializer_class = ArticleListDocumentSerializer

    lookup_field = 'id'
    filter_backends = [
        DefaultOrderingFilterBackend,
        CompoundSearchFilterBackend,
        MultiMatchSearchFilterBackend,
    ]

    multi_match_search_fields = {
        'title': None,
        'description': None,
    }

    ordering_fields = {
        'id': 'id',
        'title': 'title.raw',
        'description': 'description.raw',
    }

    ordering = ('id',)
