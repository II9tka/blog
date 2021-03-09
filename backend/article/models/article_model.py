from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone

from taggit.managers import TaggableManager

from backend.filer.models import Image
from backend.utils.models import BaseQuerySet

User = get_user_model()

__all__ = ('Article',)


class ArticleQuerySet(BaseQuerySet):
    def _all_related(self):
        return self.select_related(
            'creator', 'cover'
        ).prefetch_related(
            'tags', 'comments'
        )

    def with_all_related(self):
        return self._all_related()

    def class_object(self):
        return Article


class Article(models.Model):
    COMMON_SELECT_RELATED = ('creator', 'cover',)
    COMMON_PREFETCH_RELATED = ('tags',)

    cover = models.ForeignKey(
        Image, on_delete=models.CASCADE, verbose_name=_('Cover'), null=True
    )
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
    objects = ArticleQuerySet.as_manager()

    def get_cover(self):
        if cover := self.cover:
            return cover.image
        return None

    @property
    def lifetime(self):
        return (timezone.now() - self.created_at).days

    def __str__(self):
        return self.title if self.title else str(self.id)

    class Meta:
        ordering = ('id',)
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
