from elasticsearch_dsl import analyzer, tokenizer
from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl_drf.compat import StringField

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
    title = StringField(
        analyzer=html_strip,
        fields={
            'raw': fields.Text(analyzer='keyword'),
        }
    )
    cover = fields.FileField(
        attr='get_cover'
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
    creator = StringField(attr='creator.username')
    created_at = fields.DateField()
    updated_at = fields.DateField()
    is_published = fields.BooleanField()
    lifetime = fields.IntegerField()
    tags = StringField(
        attr='tags_indexing',
        analyzer=html_strip,
        fields={
            'raw': StringField(analyzer='keyword', multi=True),
            'suggest': fields.CompletionField(multi=True),
        },
        multi=True
    )

    class Django:
        model = Article
