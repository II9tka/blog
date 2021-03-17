from django.urls import path, include
from .routers import router, account_nested_router

urlpatterns = [
    path('', include(router.urls)),
    path('', include(account_nested_router.urls))
]
