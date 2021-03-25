from django.db import models
from django.utils.translation import gettext_lazy as _

from . import Account
from backend.filer.models import Image
from backend.utils.models import CommonRelatedModel


class AccountImage(CommonRelatedModel):
    COMMON_SELECT_RELATED = ('image',)

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, verbose_name=_('Account'), related_name='images'
    )
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, verbose_name=_('Image')
    )

    def get_image(self):
        if image := self.image:
            return image.image
        return None

    class Meta:
        ordering = ('id',)
        verbose_name = _('Account avatar')
        verbose_name_plural = _('Accounts avatar')
