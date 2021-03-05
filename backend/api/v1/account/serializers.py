from rest_framework import serializers

from enumfields.drf.serializers import EnumSupportSerializerMixin
from enumfields.drf.serializers import EnumSerializerField
from versatileimagefield.serializers import VersatileImageFieldSerializer

from backend.account.models import Account, AccountPrivacyStatus
from backend.api.v1.filer.serializers import UploadImageSerializer
from backend.filer.models import Image

__all__ = (
    'AccountListSerializer',
    'PrivateAccountDetailModelSerializer',
    'PublicAccountDetailModelSerializer',
    'OwnerAccountDetailModelSerializer',
    'UploadAvatarSerializer',
)


class AccountListSerializer(EnumSupportSerializerMixin, serializers.Serializer):
    id = serializers.IntegerField()
    id_str = serializers.CharField(source='id')
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    status_type = EnumSerializerField(AccountPrivacyStatus)
    status_type_str = serializers.CharField(source='status_type.value')
    truncate_about = serializers.CharField()
    account_url = serializers.HyperlinkedIdentityField(
        view_name='account-detail',
    )

    avatar = VersatileImageFieldSerializer(
        source='get_avatar',
        sizes=[
            ('medium_square_crop', 'crop__400x400'),
        ]
    )

    class Meta:
        fields = (
            'id',
            'id_str',
            'username',
            'first_name',
            'last_name',
            'status_type',
            'truncate_about',
            'account_url',
        )


class PrivateAccountDetailModelSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    id_str = serializers.CharField(source='id', read_only=True)
    account_url = serializers.HyperlinkedIdentityField(
        view_name='account-detail',
        read_only=True
    )
    avatar = VersatileImageFieldSerializer(
        source='get_image',
        sizes=[
            ('medium_square_crop', 'crop__400x400'),
        ]
    )
    status_type_str = serializers.CharField(source='status_type.value', read_only=True)

    class Meta:
        model = Account
        fields = (
            'id',
            'id_str',
            'username',
            'first_name',
            'last_name',
            'avatar',
            'status_type',
            'status_type_str',
            'account_url',
        )


class PublicAccountDetailModelSerializer(PrivateAccountDetailModelSerializer):
    avatar = VersatileImageFieldSerializer(
        source='get_avatar',
        sizes=[
            ('full_size', 'url'),
            ('medium_square_crop', 'crop__400x400'),
        ],
        read_only=True
    )

    class Meta(PrivateAccountDetailModelSerializer.Meta):
        fields = PrivateAccountDetailModelSerializer.Meta.fields + (
            'background_color',
            'city',
            'phone',
            'workplace',
            'work_experience',
            'about',
        )


class OwnerAccountDetailModelSerializer(PublicAccountDetailModelSerializer):
    set_avatar_url = serializers.HyperlinkedIdentityField(
        view_name='account-avatar',
        read_only=True
    )

    class Meta(PublicAccountDetailModelSerializer.Meta):
        fields = PublicAccountDetailModelSerializer.Meta.fields + (
            'set_avatar_url',
        )
        extra_kwargs = {
            'username': {'read_only': True}
        }


class UploadAvatarSerializer(UploadImageSerializer):
    def get_setattr_obj_name(self) -> str:
        return 'account'
