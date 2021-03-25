from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from enumfields import Enum, EnumIntegerField

User = get_user_model()

# TODO: create message notification


class NotificationStatus(Enum):
    UNREAD = 0
    READ = 1

    class Labels:
        UNREAD = _('Unread')
        READ = _('Read')


class Notification(models.Model):
    account = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('Account')
    )
    notification_status = EnumIntegerField(
        NotificationStatus, default=NotificationStatus.UNREAD, verbose_name=_('Notification status')
    )
