from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import GroupManager
from django.utils.translation import gettext_lazy as _

from enumfields import Enum

from backend.utils.models import BaseQuerySet

User = get_user_model()


class NotificationStatus(Enum):
    UNMUTE = 0
    MUTE = 1

    class Labels:
        UNMUTE = _('Unmute')
        MUTE = _('Mute')


class ChatManager(GroupManager.from_queryset(BaseQuerySet)):
    pass


class ChatGroupManager(GroupManager.from_queryset(BaseQuerySet)):
    pass


class Chat(models.Model):
    COMMON_SELECT_RELATED = ('creator',)
    COMMON_PREFETCH_RELATED = ('participants',)

    creator = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, related_name='chats', verbose_name=_('Creator')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created at')
    )
    participants = models.ManyToManyField(
        User, blank=True, related_name='chat_groups', verbose_name=_('Participants')
    )

    objects = ChatManager()

    @property
    def chat_name(self):
        return 'chat_%s' % self.id

    class Meta:
        ordering = ('id',)
        verbose_name = _('Chat Group')
        verbose_name_plural = _('Chat groups')
