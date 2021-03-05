import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseFileModel(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, help_text=_(
            'UUID of a file, universally Unique ID. An unique identifier '
            'generated for each file.'
        ), verbose_name=_('UUID')
    )
    filename = models.CharField(
        editable=False, null=True, blank=True, max_length=200, verbose_name=_('Filename')
    )
    created_at = models.DateTimeField(
        auto_now=True, db_index=True, help_text=_(
            'The server date and time when the file was finally '
            'processed and added to the system.'
        ), verbose_name=_('Created at')
    )
    creator = models.CharField(
        blank=True, null=True, max_length=100, help_text=_(
            'The file creator.'
        ), verbose_name=_('Creator')
    )
    mime_type = models.CharField(
        blank=True, editable=False, help_text=_(
            'The document version\'s file mimetype. MIME types are a '
            'standard way to describe the format of a file, in this case '
            'the file format of the document. Some examples: "text/plain" '
            'or "image/jpeg". '
        ), max_length=255, null=True, verbose_name=_('MIME type')
    )

    class Meta:
        abstract = True
