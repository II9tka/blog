from typing import Dict, Any, Tuple

from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from rest_framework import serializers

from backend.filer.models import Image


class UploadImageModelSerializer(serializers.ModelSerializer):
    def _get_image_args(self, validated_data) -> Tuple[str, Dict[str, Any]]:
        """
        :return ("image", {"image": InMemoryUploadedFile <...> or TemporaryUploadedFile <...>})
        """

        return tuple(*{
            field_name: value for field_name, value in validated_data.items()
            if isinstance(value, dict) and self._get_image_args(value)
            or any([isinstance(value, InMemoryUploadedFile), isinstance(value, TemporaryUploadedFile)])
        }.items())

    def _get_user(self) -> Any or None:
        if context := self.context.get('request', None):
            return context.user
        return None

    def add_image_kwargs(self) -> dict:
        return {
            'creator': self._get_user().username
        }

    def create(self, validated_data):
        fk_name, image = self._get_image_args(validated_data)

        validated_data[fk_name] = Image.objects.create(
            **image,
            **self.add_image_kwargs()
        )
        return super().create(validated_data)

    class Meta:
        model = None
