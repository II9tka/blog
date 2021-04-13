from typing import Dict, Any, Tuple, Optional

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from rest_framework import serializers

from backend.filer.models import Image

User = get_user_model()


class UploadImageModelSerializer(serializers.ModelSerializer):
    @staticmethod
    def _check_is_image(value: dict) -> bool:
        return isinstance(value, InMemoryUploadedFile) or isinstance(value, TemporaryUploadedFile)

    def _get_image_args(self, validated_data: dict) -> Tuple[str, Dict[str, Any]]:
        """
        :return ("image", {"image": InMemoryUploadedFile <...> or TemporaryUploadedFile <...>})
        """

        for field_name, value in validated_data.items():
            if isinstance(value, dict) and self._get_image_args(value) or self._check_is_image(value):
                return field_name, value

    def _get_user(self) -> Optional[User]:
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
