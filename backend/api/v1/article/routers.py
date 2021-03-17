from rest_framework_nested import routers

from .views import ArticleViewSet, ArticleCommentViewSet, ArticleCommentLikeViewSet, ArticleCoverViewSet

router = routers.DefaultRouter()
router.register(r'', ArticleViewSet, basename='article')

article_nested_router = routers.NestedDefaultRouter(router, r'', lookup='article')
article_nested_router.register(r'comments', ArticleCommentViewSet, basename='article-comments')
article_nested_router.register(r'cover', ArticleCoverViewSet, basename='article-cover')

article_comment_nested_router = routers.NestedDefaultRouter(article_nested_router, r'comments', lookup='comment')
article_comment_nested_router.register(r'likes', ArticleCommentLikeViewSet, basename='article-comments-likes')
