from django.db import models


class BaseQuerySet(models.QuerySet):
    # TODO: Maybe it should be transferred to the model as base "objects"

    def class_object(self):
        """
        To use:
            return class where "objects" will be redefined
        """
        return None

    def _common_select_related(self):
        class_object = self.class_object()
        qs = self.all()
        if hasattr(class_object, 'COMMON_SELECT_RELATED'):
            qs = qs.select_related(*class_object.COMMON_SELECT_RELATED)
        if hasattr(class_object, 'COMMON_PREFETCH_RELATED'):
            qs = qs.prefetch_related(*class_object.COMMON_PREFETCH_RELATED)
        return qs

    def with_related(self):
        return self._common_select_related()
