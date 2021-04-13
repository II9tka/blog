from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from ..validators import validate_comment
from . import Article

User = get_user_model()

__all__ = (
    'ArticleComment',
    'ArticleCommentLike',
)


class ArticleComment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, verbose_name=_('Article'), related_name='comments'
    )
    creator = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, verbose_name=_('Comment creator')
    )
    text = models.TextField(
        max_length=5000, verbose_name=_('Comment text'), validators=[validate_comment]
    )
    created_at = models.DateField(
        auto_now_add=True, verbose_name=_('Created at')
    )
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True, related_name="children", verbose_name=_('Parent')
    )

    def __str__(self):
        return 'Comment %i for Article %i' % (self.id, self.article.id)

    class Meta:
        ordering = ('id',)
        verbose_name = _('Article comment')
        verbose_name_plural = _('Article comments')


class ArticleCommentLike(models.Model):
    creator = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, verbose_name=_('Like creator')
    )
    comment = models.ForeignKey(
        ArticleComment, on_delete=models.CASCADE, verbose_name=_('Comment'), related_name='likes'
    )

    def __str__(self):
        return 'Like %i for Comment %i' % (self.id, self.comment.id)

    class Meta:
        ordering = ('id',)
        verbose_name = _('Article comment like')
        verbose_name_plural = _('Article comment likes')
