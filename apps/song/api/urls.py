from django.urls import path, include

from rest_framework_nested import routers

from .views import (SongViewSet,
                    SongCommentViewSet,

                    SongRequestManager,
                    SongRequestViewSet,
                    SongRequestCommentViewSet,)

song_router = routers.DefaultRouter()
song_router.register(r'songs', SongViewSet)
song_comment_router = routers.NestedDefaultRouter(song_router, r'songs', lookup='song')
song_comment_router.register(r'comments', SongCommentViewSet, basename='song-comments')


song_request_router = routers.DefaultRouter()
song_request_router.register(r'playlist/songs', SongRequestViewSet, basename='playlist-songs')
song_request_router.register(r'playlist', SongRequestManager)
song_request_comment_router = routers.NestedDefaultRouter(song_request_router, r'playlist/songs', lookup='playlist_song')
song_request_comment_router.register(r'comments', SongRequestCommentViewSet, basename='playlist-song-comments')

urlpatterns = [
    path('', include(song_router.urls)),
    path('', include(song_comment_router.urls)),

    path('', include(song_request_router.urls)),
    path('', include(song_request_comment_router.urls)),
]
