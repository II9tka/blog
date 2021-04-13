from django.utils.translation import gettext_lazy as _

from rest_framework import serializers, status


def get_obj_or_raise_error(
        model=None,
        validated_data: dict = None,
        context: dict = None,
        pk_args: str = '',
):
    pk = context['view'].kwargs.get(pk_args, None)
    model_obj = model.objects.filter(pk=pk)

    if model_obj.exists():
        validated_data['%s' % pk_args.split('_')[0]] = model_obj.first()
    else:
        raise serializers.ValidationError(
            {
                "message": _("%s does not exist or not available.") % model.__name__,
                'status': status.HTTP_400_BAD_REQUEST
            }
        )


class RecursiveChildrenSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data
