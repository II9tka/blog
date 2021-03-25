from rest_framework import serializers

from enumfields.drf.serializers import EnumSupportSerializerMixin
from versatileimagefield.serializers import VersatileImageFieldSerializer

from backend.account.models import Account, AccountImage

__all__ = (
    'AccountImageSerializer',
    'AccountListModelSerializer',
    'PrivateAccountDetailModelSerializer',
    'PublicAccountDetailModelSerializer',
)

from backend.api.v1.filer.utils.serializers import UploadImageModelSerializer
from backend.utils.serializers import get_obj_or_raise_error


class AccountImageSerializer(UploadImageModelSerializer):
    image = VersatileImageFieldSerializer(
        source='image.image',
        sizes='public_account_image'
    )

    def create(self, validated_data):
        get_obj_or_raise_error(
            model=Account, pk_args='account_pk', context=self.context, validated_data=validated_data
        )
        return super().create(validated_data)

    class Meta:
        model = AccountImage
        exclude = ('account',)


class AccountListModelSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    id_str = serializers.CharField(source='id', read_only=True)
    status_type_str = serializers.CharField(source='status_type', read_only=True)
    account_url = serializers.HyperlinkedIdentityField(
        view_name='account-detail',
    )
    gender_str = serializers.CharField(source='gender', read_only=True)

    last_image = VersatileImageFieldSerializer(
        sizes='private_account_image'
    )

    class Meta:
        model = Account
        fields = (
            'id',
            'id_str',
            'last_image',
            'username',
            'first_name',
            'last_name',
            'status_type',
            'status_type_str',
            'gender',
            'gender_str',
            'truncate_about',
            'account_url',
        )
        extra_kwargs = {
            'username': {'read_only': True}
        }


class PrivateAccountDetailModelSerializer(AccountListModelSerializer):
    class Meta(AccountListModelSerializer.Meta):
        fields = AccountListModelSerializer.Meta.fields + (
            'status_type',
            'status_type_str',
        )


class PublicAccountDetailModelSerializer(PrivateAccountDetailModelSerializer):
    last_image = VersatileImageFieldSerializer(
        sizes='public_account_image',
        read_only=True
    )
    images = AccountImageSerializer(read_only=True, many=True)

    class Meta(PrivateAccountDetailModelSerializer.Meta):
        fields = PrivateAccountDetailModelSerializer.Meta.fields + (
            'background_color',
            'city',
            'phone_number',
            'workplace',
            'work_experience',
            'about',
            'images',
        )
