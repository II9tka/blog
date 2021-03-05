from django.urls import path, include
from .routers import router, article_nested_router

urlpatterns = [
    path('', include(router.urls)),
    path('', include(article_nested_router.urls)),
]
