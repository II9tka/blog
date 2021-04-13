from django.db.models import Q
from django_auto_prefetching import AutoPrefetchViewSetMixin
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from backend.chat.models import Chat
from .serializers import ChatModelSerializer


class ChatGroupViewSet(AutoPrefetchViewSetMixin,
                       mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = ChatModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user

        return Chat.objects.filter(
            Q(participants__exact=user) | Q(creator=user)
        )

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
