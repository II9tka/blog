from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.account.models import Account, AccountPrivacyStatus

from .serializers import (
    AccountListSerializer,
    PrivateAccountDetailModelSerializer,
    PublicAccountDetailModelSerializer,
    OwnerAccountDetailModelSerializer,
    UploadAvatarSerializer
)

__all__ = ('AccountViewSet',)

STATUS = AccountPrivacyStatus


class AccountViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Account.objects.with_related()

    def get_serializer_class(self):
        if self.action == 'list':
            return AccountListSerializer
        elif self.action == 'avatar':
            return UploadAvatarSerializer
        else:
            account = self.get_object()
            user = self.request.user
            if user.is_authenticated and account == user:
                return OwnerAccountDetailModelSerializer
            elif account.status_type == STATUS.PUBLIC:
                return PublicAccountDetailModelSerializer
            elif account.status_type == STATUS.PRIVATE:
                return PrivateAccountDetailModelSerializer

    @action(methods=['POST'], detail=True)
    def avatar(self, request, pk=None):
        account = self.get_object()
        serializer = self.get_serializer(data=request.FILES)
        serializer.is_valid(raise_exception=True)
        serializer.save(account=account)
        return Response(serializer.data)
