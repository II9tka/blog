from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from enumfields import Enum

User = get_user_model()


# TODO: create message notification (redis)


class NotificationStatus(Enum):
    UNREAD = 0
    READ = 1

    class Labels:
        UNREAD = _('Unread')
        READ = _('Read')
