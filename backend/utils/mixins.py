from typing import Any

from django.db.models import prefetch_related_objects
from rest_framework.relations import ManyRelatedField, RelatedField
from rest_framework.serializers import ListSerializer


def _prefetch(serializer_class: Any, parent_prefix: str = ''):
    prefetch_related = set()

    try:
        fields = getattr(serializer_class, "child", serializer_class).fields.fields.items()
    except AttributeError:
        return prefetch_related

    for related_name, field in fields:
        prefetch_format = f'{parent_prefix}__{related_name}' if parent_prefix else related_name

        if isinstance(field, RelatedField) and parent_prefix:
            prefetch_related.add(prefetch_format)

        elif isinstance(field, (ListSerializer, ManyRelatedField)):
            prefetch_related.add(prefetch_format)

            nested_field = getattr(field, "child_relation", field)
            prefetch_related |= _prefetch(
                serializer_class=nested_field,
                parent_prefix=prefetch_format
            )

    return prefetch_related


class PrefetchedFieldsSerializerMixin:
    def make_prefetch(self):
        return _prefetch(self)

    def to_representation(self, instance):
        return super().to_representation(self._prefetch_fields(instance))

    def _prefetch_fields(self, instance):
        if not hasattr(instance, "_prefetched_objects_cache"):
            prefetch_fields = self.make_prefetch()
            prefetch_related_objects([instance], *prefetch_fields)
        return instance
