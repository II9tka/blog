from typing import Union, Dict

from django.db.models import Prefetch
from django.http import HttpResponse
from django_auto_prefetching import AutoPrefetchViewSetMixin
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict

from backend.account.models import Account
from backend.article.models import (
    Article,
    ArticleComment,
)
from backend.article.models.article_cover_model import ArticleCover

from .serializers import (
    ArticleListModelSerializer, ArticleDetailModelSerializer,
    ArticleCommentModelSerializer,
    ArticleCommentLikeModelSerializer, ArticleCoverModelSerializer,
)


class ArticleCommentLikeViewSet(mixins.CreateModelMixin,
                                viewsets.GenericViewSet):
    serializer_class = ArticleCommentLikeModelSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @staticmethod
    def get_response(data: ReturnDict, headers: Union[Dict[str, str], dict]) -> HttpResponse:
        if data['id']:
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(status=status.HTTP_204_NO_CONTENT, headers=headers)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return self.get_response(serializer.data, headers)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class ArticleViewSet(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Article.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListModelSerializer
        else:
            return ArticleDetailModelSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(methods=['GET'], detail=False, url_path='most-common-tags')
    def most_common_tags(self, request, *args, **kwargs):
        queryset = Article.tags.most_common()[:20]
        return Response(queryset.values('id', 'name'))


class ArticleCommentViewSet(mixins.CreateModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = ArticleCommentModelSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return ArticleComment.objects.filter(
            article=self.kwargs['article_pk'],
            article__creator=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class ArticleCoverViewSet(mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = ArticleCoverModelSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
