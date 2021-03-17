from rest_framework_nested import routers

from .views import AccountViewSet, AccountImageViewSet

router = routers.DefaultRouter()
router.register(r'', AccountViewSet)

account_nested_router = routers.NestedDefaultRouter(router, r'', lookup='account')
account_nested_router.register(r'images', AccountImageViewSet, basename='account-images')
