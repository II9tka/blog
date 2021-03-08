from rest_framework.routers import SimpleRouter

from .views import ArticleSearchViewSet

router = SimpleRouter()
router.register(r'articles', viewset=ArticleSearchViewSet, basename='articles_search')
