from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from backend.utils.models import CommonRelatedModel

User = get_user_model()


class Message(CommonRelatedModel):
    COMMON_SELECT_RELATED = ('sender',)

    timestamp = models.DateTimeField(
        auto_now_add=True, help_text=_(
            'Message creation time.'
        ), verbose_name=_('Timestamp')
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('Sender')
    )
    text = models.TextField(
        max_length=2000, verbose_name=_('Text')
    )

    def __str__(self):
        return 'Message %i. Sender: %s. Text: %s. ' % (self.id, self.sender, self.text[:100])
