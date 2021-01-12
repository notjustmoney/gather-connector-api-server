from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (SongViewSet, SongRequestViewSet,
                    MySongRequestListViewSet,
                    SongCommentListAPIView, SongCommentDetailAPIView,
                    SongRequestCommentViewSet,
                    SongLikeAPIView, CommentLikeAPIView,
                    SongRequestCommentListAPIView, SongRequestCommentDetailAPIView)

router = DefaultRouter()
router.register(r'songs', SongViewSet)
router.register(r'playlist/songs/me', MySongRequestListViewSet)
# router.register(r'playlist/songs/<int:song_request_id>/comments', SongRequestCommentViewSet)
router.register(r'playlist/songs', SongRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(r'songs/<int:pk>/like/', SongLikeAPIView.as_view()),
    path(r'songs/<int:song_id>/comments/', SongCommentListAPIView.as_view()),
    path(r'songs/<int:song_id>/comments/<int:comment_id>/', SongCommentDetailAPIView.as_view(), name='comment-detail'),
    path(r'songs/<int:song_id>/comments/<int:comment_id>/like/', CommentLikeAPIView.as_view()),
    path(r'playlist/songs/<int:song_request_id>/comments/', SongRequestCommentListAPIView.as_view()),
    path(r'playlist/songs/<int:song_request_id>/comments/<int:comment_id>/', SongRequestCommentDetailAPIView.as_view()),
    path(r'playlist/songs/<int:pk>/like', SongLikeAPIView.as_view()),
]
