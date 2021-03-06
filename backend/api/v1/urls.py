from django.urls import path, include

urlpatterns = [
    path('accounts/', include('backend.api.v1.account.urls')),
    path('articles/', include('backend.api.v1.article.urls')),
    path('phone_login/', include('phone_login.urls'), name='phone_login'),
    path('search/', include('backend.api.v1.search.urls')),
    path('chats/', include('backend.api.v1.chat.urls'))
]
