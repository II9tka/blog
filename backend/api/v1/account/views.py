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
            if account.status_type == STATUS.PUBLIC or self.request.user == account:
                return PublicAccountDetailModelSerializer
            elif account.status_type == STATUS.PRIVATE:
                return PrivateAccountDetailModelSerializer

    def get_object(self):
        if self.kwargs.get('pk', None) == 'me' and self.request.user.is_authenticated:
            return self.request.user
        return super().get_object()


class AccountImageViewSet(mixins.DestroyModelMixin,
                          mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = AccountImageSerializer
    permission_classes = (IsAuthenticated,)
