from django.urls import path, include

from rest_framework_nested import routers

from .views import (SongViewSet,
                    SongCommentViewSet,

                    SongRequestManager,
                    SongRequestViewSet,
                    SongRequestCommentViewSet,

                    HistoryViewSst,
                    StatisticViewSet,)

song_router = routers.DefaultRouter()
song_router.register(r'songs', SongViewSet)
song_comment_router = routers.NestedDefaultRouter(song_router, r'songs', lookup='song')
song_comment_router.register(r'comments', SongCommentViewSet, basename='song-comments')


song_request_router = routers.DefaultRouter()
song_request_router.register(r'songs', SongRequestViewSet, basename='playlist-songs')
song_request_router.register(r'history', HistoryViewSst)
song_request_router.register(r'', SongRequestManager)

song_request_comment_router = routers.NestedDefaultRouter(song_request_router, r'songs', lookup='playlist_song')
song_request_comment_router.register(r'comments', SongRequestCommentViewSet, basename='playlist-song-comments')

statistic_router = routers.DefaultRouter()
statistic_router.register(r'', StatisticViewSet, basename='stats')

urlpatterns = [
    path('', include(song_router.urls)),
    path('', include(song_comment_router.urls)),

    path('playlist/', include(song_request_router.urls)),
    path('playlist/', include(song_request_comment_router.urls)),

    path('stats/', include(statistic_router.urls)),
]
