from django.db import models
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from enumfields import Enum, EnumIntegerField

from backend.filer.models import Image


class NotificationStatus(Enum):
    UNMUTE = 0
    MUTE = 1

    class Labels:
        UNMUTE = _('Unmute')
        MUTE = _('Mute')


class ChatGroup(Group):
    notification_status = EnumIntegerField(
        NotificationStatus, default=NotificationStatus.UNMUTE, help_text=_(
            'Message notifications. '
            'Disable if MUTE status, Enable if UNMUTE status.'
        ), verbose_name=_('Notifications')
    )
    icon = models.ForeignKey(
        Image, on_delete=models.CASCADE, verbose_name=_('Icon')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created at')
    )

    class Meta:
        ordering = ('id',)
        verbose_name = _('Chat Group')
        verbose_name_plural = _('Chat groups')
