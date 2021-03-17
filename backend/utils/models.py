from django.db import models


class BaseQuerySet(models.QuerySet):

    def _common_select_related(self):
        model = self.model
        qs = self.all()

        if getattr(model, 'COMMON_SELECT_RELATED', None):
            qs = qs.select_related(*model.COMMON_SELECT_RELATED)
        if getattr(model, 'COMMON_PREFETCH_RELATED', None):
            qs = qs.prefetch_related(*model.COMMON_PREFETCH_RELATED)
        return qs

    def with_common_related(self):
        return self._common_select_related()


class CommonRelatedModel(models.Model):
    objects = BaseQuerySet.as_manager()

    class Meta:
        abstract = True
