from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import Chat

User = get_user_model()


class Message(models.Model):
    timestamp = models.DateTimeField(
        auto_now_add=True, help_text=_(
            'Message creation time.'
        ), verbose_name=_('Timestamp')
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('Sender')
    )
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, verbose_name=_('Chat room'), related_name='messages', null=True
    )
    text = models.TextField(
        max_length=2000, verbose_name=_('Text')
    )

    def __str__(self):
        return 'Message %i. Sender: %s. Text: %s. ' % (self.id, self.sender, self.text[:100])
