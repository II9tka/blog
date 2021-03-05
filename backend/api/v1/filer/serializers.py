from rest_framework import serializers

from backend.filer.models import Image


class UploadRelatedImageSerializer(serializers.ModelSerializer):
    def get_setattr_obj_name(self) -> str:
        return ''

    def _get_username(self):
        if context := self.context.get('request', None):
            return context.user.username
        return None

    def create(self, validated_data):
        image_field = self.get_setattr_obj_name()
        file = validated_data.pop(image_field, None)
        if file:
            image = Image.objects.create(**{
                'creator': self._get_username(),
                'image': file
            })
            validated_data = {
                **validated_data,
                image_field: image
            }
        return super().create(validated_data)


class UploadImageSerializer(UploadRelatedImageSerializer):
    def _get_image_field_name(self, obj):
        model = self.Meta.model
        fields = getattr(obj, '_meta').get_fields()

        for field in fields:
            if field.many_to_one and field.related_model == model:
                return field.name

    def save(self, **kwargs):
        image = None
        setattr_obj_name = self.get_setattr_obj_name()

        if obj := kwargs.pop(setattr_obj_name, None):
            image = super().save()
            related_image_field = self._get_image_field_name(obj)
            setattr(obj, related_image_field, image)
            obj.save()
        return image

    def create(self, validated_data):
        validated_data['creator'] = self._get_username()
        return super().create(validated_data)

    class Meta:
        fields = ('image',)
        model = Image
