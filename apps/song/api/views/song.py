from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.common.permissions import IsOwnerOrReadOnly

from apps.song.models import Song, Comment, LikeSong, LikeComment

from ..serializers import (SongSerializer,
                           SongCommentSerializer,
                           LikeSongSerializer,
                           LikeCommentSerializer)

from .like import like_song, like_comment


class SongViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    @action(detail=True, methods=['post'], url_path='like')
    def like(self, request, pk=None):
        user = request.user
        song_pk = pk
        song = get_object_or_404(Song, pk=song_pk)
        return like_song(request, user, song)


class SongCommentViewSet(viewsets.ModelViewSet):
    serializer_class = SongCommentSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get_queryset(self):
        song_pk = self.kwargs.get('song_pk', None)
        return Comment.objects.filter(song=song_pk)

    def perform_create(self, serializer):
        user = self.request.user
        song_pk = self.kwargs.get('song_pk', None)
        song = get_object_or_404(Song, pk=song_pk)
        serializer.save(user=user, song=song)

    @action(detail=True, methods=['post'], url_path='like')
    def like(self, request, song_pk=None, pk=None):
        user = request.user
        comment_pk = pk
        comment = get_object_or_404(Comment, pk=comment_pk, song=song_pk)
        return like_comment(request, user, comment)
