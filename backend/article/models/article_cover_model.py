from django.db import models
from django.utils.translation import gettext_lazy as _

from backend.article.models import Article
from backend.filer.models import Image


class ArticleCover(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, verbose_name=_('Article cover'), related_name='covers'
    )
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, verbose_name=_('Image')
    )

    def get_image(self):
        if image := self.image:
            return image.image
        return None

    def __str__(self):
        return 'Article cover %s' % self.image

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if article_covers := self.article.covers:
            article_covers.all().delete()
        return super().save()

    class Meta:
        ordering = ('id',)
        verbose_name = _('Article cover')
        verbose_name_plural = _('Article covers')
