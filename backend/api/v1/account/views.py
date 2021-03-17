from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from backend.account.models import Account, AccountPrivacyStatus

from .serializers import (
    AccountListModelSerializer,
    PrivateAccountDetailModelSerializer,
    PublicAccountDetailModelSerializer,
    AccountImageSerializer,
)

__all__ = ('AccountViewSet',
           'AccountImageViewSet',)

STATUS = AccountPrivacyStatus


class AccountViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Account.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AccountListModelSerializer
        else:
            account = self.get_object()
            if account.status_type == STATUS.PUBLIC:
                return PublicAccountDetailModelSerializer
            elif account.status_type == STATUS.PRIVATE:
                return PrivateAccountDetailModelSerializer


class AccountImageViewSet(mixins.DestroyModelMixin,
                          mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = AccountImageSerializer
    permission_classes = (IsAuthenticated,)
