from rest_framework_nested import routers

from .views import ArticleViewSet, ArticleImageViewSet

router = routers.DefaultRouter()
router.register(r'', ArticleViewSet)

article_nested_router = routers.NestedDefaultRouter(router, r'', lookup='article')
article_nested_router.register(r'images', ArticleImageViewSet, basename='article-images')
