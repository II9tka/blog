from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from enumfields import Enum, EnumIntegerField

User = get_user_model()


class ConnectionStatus(Enum):
    OFFLINE = 0
    ONLINE = 1

    class Labels:
        OFFLINE = _('Offline')
        ONLINE = _('Online')


class AccountConnectionHistory(models.Model):
    account = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('account'), related_name='connections'
    )
    device_id = models.CharField(max_length=100, help_text=_(
        'Unique ID of the user\'s device.'
    ), verbose_name=_('Device ID'))
    connection_status = EnumIntegerField(
        ConnectionStatus, default=ConnectionStatus.OFFLINE, help_text=_(
            'Account connection status.'
        ), verbose_name=_('Connection status')
    )
    last_connection = models.DateTimeField(auto_now=True, verbose_name=_('Last connection'))

    class Meta:
        unique_together = (('account', 'device_id'),)
