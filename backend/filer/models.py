import logging

from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from versatileimagefield.fields import VersatileImageField

from .base import BaseFileModel
from .services import upload_to

logger = logging.getLogger(__name__)

__all__ = ('Image',)


class Image(BaseFileModel):
    image = VersatileImageField(
        upload_to=upload_to, width_field='width', height_field='height', verbose_name=_('Image')
    )
    height = models.PositiveIntegerField(
        blank=True, null=True, verbose_name=_('Image height'), editable=False
    )
    width = models.PositiveIntegerField(
        blank=True, null=True, verbose_name=_('Image Width'), editable=False
    )

    def _definition_mime_type(self):
        import magic

        image = self.image
        mime_type = magic.from_buffer(image.read(), mime=True)
        return mime_type

    def width_height(self):
        return self.width, self.height

    def save(self, *args, **kwargs):
        self.mime_type = self._definition_mime_type()

        existing_images = Image.objects.filter(
            image='%s/%s/%s' % (self.creator, self.image.name.split('.')[-1], self.image.name)
        )
        with transaction.atomic():
            for existing_image in existing_images:
                existing_image.image.delete_sized_images()
                existing_image.delete()
                logger.info(
                    'File {filename} has been cleared.'.format(filename=existing_image)
                )

        super().save(*args, **kwargs)

    def __str__(self):
        if self.image:
            return '%s: %i x %i' % (self.image.name, self.height, self.width)
        return str(self.id)

    class Meta:
        ordering = ('id',)
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
