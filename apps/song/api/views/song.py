import datetime

from django.shortcuts import get_object_or_404
from django.utils.timezone import utc

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.common.permissions import IsOwnerOrReadOnly

from apps.song.models import Song, Comment

from ..serializers import SongSerializer, SongCommentSerializer

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
        return Comment.objects.filter(song=song_pk, deleted_at__isnull=True)

    def destroy(self, request, *args, **kwargs):
        comment_pk = kwargs.get('pk', None)
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.deleted_at:
            return Response({"message": '처리할 수 없는 요청입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        comment.deleted_at = datetime.datetime.utcnow().replace(tzinfo=utc)
        comment.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

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
