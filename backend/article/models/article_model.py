from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone

from taggit.managers import TaggableManager

User = get_user_model()

__all__ = ('Article',)


class Article(models.Model):
    title = models.CharField(
        max_length=100, default='', blank=True, verbose_name=_('Title')
    )
    description = models.TextField(
        max_length=4000, default='', blank=True, verbose_name=_('Description')
    )
    short_description = models.TextField(
        max_length=400, default='', blank=True, verbose_name=_('Short description')
    )
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='articles', verbose_name=_('Creator')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created at'), editable=False
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('Updated at'), editable=False
    )
    is_published = models.BooleanField(
        default=False, verbose_name=_('Is published')
    )

    tags = TaggableManager()

    def get_cover(self):
        if cover := self.covers.last():
            return cover.get_image()
        return None

    @property
    def lifetime(self):
        return (timezone.now() - self.created_at).days

    @property
    def tags_indexing(self):
        """Tags for indexing.

        Used in Elasticsearch indexing.
        """
        return [tag.name for tag in self.tags.all()]

    def __str__(self):
        return self.title if self.title else str(self.id)

    class Meta:
        ordering = ('id',)
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
