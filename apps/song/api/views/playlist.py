from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from apps.common.permissions import IsOwnerOrReadOnly

from apps.song.models import SongRequest, Comment

from ..serializers import SongRequestSerializer, SongCommentSerializer

from .like import like_song, like_comment


class SongRequestViewSet(viewsets.ModelViewSet):
    queryset = SongRequest.objects.all()
    serializer_class = SongRequestSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        user = request.user
        song_requests = SongRequest.objects.filter(user=user)
        serializer = SongRequestSerializer(song_requests, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='like')
    def like(self, request, pk=None):
        user = request.user
        song_request_pk = pk
        song_request = get_object_or_404(SongRequest, pk=song_request_pk)
        song = song_request.song
        return like_song(request, user, song)


class SongRequestCommentViewSet(viewsets.ModelViewSet):
    serializer_class = SongCommentSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get_queryset(self):
        song_request_pk = self.kwargs.get('playlist_song_pk', None)
        song_request = get_object_or_404(SongRequest, pk=song_request_pk)
        song = song_request.song
        return Comment.objects.filter(song=song)

    def perform_create(self, serializer):
        user = self.request.user
        song_request_id = self.kwargs.get('playlist_song_pk', None)
        song_request = get_object_or_404(SongRequest, pk=song_request_id)
        song = song_request.song
        serializer.save(user=user, song=song)

    @action(detail=True, methods=['post'], url_path='like')
    def like(self, request, playlist_song_pk=None, pk=None):
        user = request.user
        song_request = get_object_or_404(SongRequest, pk=playlist_song_pk)
        song = song_request.song
        comment_pk = pk
        comment = get_object_or_404(Comment, pk=comment_pk, song=song.id)
        return like_comment(request, user, comment)
