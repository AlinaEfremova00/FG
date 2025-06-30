from django.urls import path, include
from users.views_follow import FollowViewSet

follow = FollowViewSet.as_view({
    'get': 'list',
    'post': 'subscribe'
})

unsubscribe = FollowViewSet.as_view({
    'post': 'unsubscribe'
})

urlpatterns = [
    path('follows/', follow, name='follows'),
    path('follows/unsubscribe/', unsubscribe, name='unsubscribe'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
