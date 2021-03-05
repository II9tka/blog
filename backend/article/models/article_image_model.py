from django.db import models
from django.utils.translation import gettext_lazy as _

from backend.filer.models import Image
from backend.utils.models import BaseQuerySet
from . import Article


class ArticleImageQuerySet(BaseQuerySet):
    def _all_related(self):
        return self.select_related(
            'article', 'image'
        )

    def with_all_related(self):
        return self._all_related()

    def class_object(self):
        return ArticleImage


class ArticleImage(models.Model):
    COMMON_SELECT_RELATED = ('image',)

    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, verbose_name=_('Article image')
    )
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, verbose_name=_('Article'), related_name='images'
    )

    def get_image(self):
        if image := self.image:
            return image.image
        return None

    objects = ArticleImageQuerySet.as_manager()

    def __str__(self):
        return 'Image: {id} {size} {mime_type}'.format(
            id=self.id, size=self.image.width_height, mime_type=self.image.mime_type
        )

    class Meta:
        ordering = ('id',)
        verbose_name = _('Article Image')
        verbose_name_plural = _('Article Images')
