from typing import Optional

from django.conf import settings
from versatileimagefield.fields import VersatileImageField
from versatileimagefield.serializers import VersatileImageFieldSerializer
from versatileimagefield.utils import build_versatileimagefield_url_set

from backend.filer.models import Image

IMAGE_MODEL = Image
MEDIA_URL = settings.MEDIA_URL


class ElasticSearchVersatileImageFieldSerializer(VersatileImageFieldSerializer):
    @staticmethod
    def _check_is_path(value: str) -> bool:
        media_url = MEDIA_URL

        return isinstance(value, str) and media_url in value

    @staticmethod
    def _convert_path_to_image(value: str) -> Optional[VersatileImageField]:
        return convert_path_to_image(value)

    def to_native(self, value):
        context_request = None
        if self._check_is_path(value):
            value = self._convert_path_to_image(value)
            if self.context:
                context_request = self.context.get('request', None)
            return build_versatileimagefield_url_set(
                value,
                self.sizes,
                request=context_request
            )
        return None


def convert_path_to_image(media_image_path: str) -> VersatileImageField:
    """
    From path /media/image.jpg to image.jpg file.
    """
    media_url, image_model = MEDIA_URL, IMAGE_MODEL

    image_path = media_image_path.replace(media_url, '')
    fake_image = image_model(image=image_path)
    return fake_image.image
