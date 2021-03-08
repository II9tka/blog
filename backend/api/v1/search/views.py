from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_EXCLUDE,
    LOOKUP_QUERY_CONTAINS,
    LOOKUP_QUERY_STARTSWITH
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
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
