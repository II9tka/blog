from rest_framework_nested import routers

from backend.api.v1.chat.views import ChatGroupViewSet

router = routers.DefaultRouter()
router.register(r'', ChatGroupViewSet, basename='chats')
