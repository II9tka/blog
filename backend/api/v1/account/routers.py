from rest_framework_nested import routers

from .views import AccountViewSet

router = routers.DefaultRouter()
router.register(r'', AccountViewSet)
