from elasticsearch_dsl import analyzer, tokenizer
from django_elasticsearch_dsl import Document, Index, fields

from .models import Article

ARTICLE_INDEX = Index('article')

ARTICLE_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1,
    max_ngram_diff=16
)

html_strip = analyzer(
    'html_strip',
    tokenizer=tokenizer('serializer', 'nGram', min_gram=2, max_gram=6),
    filter=[
        "lowercase",
        "stop",
        "snowball",
        "russian_morphology",
        "english_morphology",
        "ngram"
    ],
    char_filter=["html_strip"]
)


@ARTICLE_INDEX.doc_type
class ArticleDocument(Document):
    id = fields.IntegerField(attr='id')
    title = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.Text(analyzer='keyword'),
        }
    )
    description = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )
    short_description = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )
    creator = fields.IntegerField(attr='creator_id')
    created_at = fields.DateField()
    updated_at = fields.DateField()

    class Django:
        model = Article
