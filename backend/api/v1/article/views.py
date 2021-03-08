from django.db import models

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.article.models import (
    Article,
    ArticleImage,
    ArticleComment,
)

from .serializers import (
    ArticleListModelSerializer, ArticleDetailModelSerializer, UploadArticleCoverSerializer,
    UploadArticleImageSerializer,
    ArticleCommentModelSerializer,
    ArticleCommentLikeModelSerializer,
)


class ArticleCommentLikeViewSet(mixins.CreateModelMixin,
                                viewsets.GenericViewSet):
    serializer_class = ArticleCommentLikeModelSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    # TODO: change status code if like delete


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.with_related()

    def get_serializer_class(self):
        if self.action == 'cover':
            return UploadArticleCoverSerializer
        elif self.action == 'list':
            return ArticleListModelSerializer
        else:
            return ArticleDetailModelSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(methods=['GET'], detail=False, url_path='most-common-tags')
    def most_common_tags(self, request, *args, **kwargs):
        queryset = Article.tags.most_common()[:20]
        return Response(queryset.values('id', 'name'))

    @action(methods=['POST'], detail=True, )
    def cover(self, request, pk=None):
        article = self.get_object()
        serializer = self.get_serializer(data=request.FILES)
        serializer.is_valid(raise_exception=True)
        serializer.save(article=article)
        return Response(serializer.data)


class ArticleImageViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = UploadArticleImageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return ArticleImage.objects.with_all_related().filter(
            article=self.kwargs['article_pk'],
            article__creator=self.request.user
        )


class ArticleCommentViewSet(mixins.CreateModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = ArticleCommentModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return ArticleComment.objects.with_related().filter(
            article=self.kwargs['article_pk'],
            article__creator=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
