from rest_framework import serializers, status
from django.utils.translation import gettext_lazy as _


def get_obj_or_raise_error(
        model=None,
        validated_data: dict = None,
        context: dict = None,
        pk_args: str = '',
):
    pk = context['view'].kwargs.get(pk_args, None)
    model_obj = model.objects.filter(pk=pk)
    if model_obj.exists():
        validated_data['%s' % model.__name__.lower()] = model_obj.first()
    else:
        raise serializers.ValidationError(
            {
                "message": _("%s does not exist or not available.") % model.__name__,
                'status': status.HTTP_400_BAD_REQUEST
            }
        )
