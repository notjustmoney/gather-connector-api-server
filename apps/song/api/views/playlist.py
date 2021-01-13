import datetime

from django.db.models import Max
from django.shortcuts import get_object_or_404
from django.utils.timezone import utc

from rest_framework import viewsets, status, exceptions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from apps.common.permissions import IsOwnerOrReadOnly

from apps.song.models import SongRequest, Comment, Song

from ..serializers import SongRequestSerializer, SongCommentSerializer

from .like import like_song, like_comment


class SongRequestViewSet(viewsets.ModelViewSet):
    queryset = SongRequest.objects.filter(deleted_at__isnull=True, played_at__isnull=True).order_by('requested_at')
    serializer_class = SongRequestSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        song_request_pk = kwargs.get('pk', None)
        try:
            song_request = self.get_queryset().get(pk=song_request_pk)
        except SongRequest.DoesNotExist:
            return Response({'message': '처리할 수 없는 요청입니다,'}, status=status.HTTP_204_NO_CONTENT)
        song_request.deleted_at = datetime.datetime.utcnow().replace(tzinfo=utc)
        song_request.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

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
        if song_request.deleted_at:
            raise exceptions.NotFound('삭제된 신청곡입니다.')
        song = song_request.song
        return Comment.objects.filter(song=song, deleted_at__isnull=True)

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


class SongRequestManager(viewsets.ReadOnlyModelViewSet):
    queryset = SongRequest.objects.filter(deleted_at__isnull=True, played_at__isnull=True)
    serializer_class = SongRequestSerializer
    # permission_classes = admin only

    def list(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(request.method)

    def retrieve(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(request.method)

    @action(detail=False, methods=['post'], url_path='play')
    def play(self, request):
        requests = self.get_queryset().order_by('requested_at')
        songs = Song.objects.filter(id__in=requests.values('song_id')).annotate(max_like=Max('like_cnt')).order_by('-max_like')
        if len(songs) == 0:
            return Response({"message": "대기열이 비어있습니다."}, status=status.HTTP_400_BAD_REQUEST)
        song_id = songs[0].id
        songs[0].play_cnt += 1
        songs[0].save()

        print('here!', song_id)
        target = requests.filter(song_id=song_id)[0]
        target.played_at = datetime.datetime.utcnow().replace(tzinfo=utc)
        target.save()
        serializer = self.get_serializer(target)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='clear')
    def clear(self, request):
        if len(self.get_queryset()) == 0:
            return Response({"message": "대기열이 비어있습니다."}, status=status.HTTP_400_BAD_REQUEST)
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.get_queryset().update(deleted_at=now)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class HistoryViewSst(viewsets.ReadOnlyModelViewSet):
    queryset = SongRequest.objects.filter(deleted_at__isnull=True, played_at__isnull=False)
    serializer_class = SongRequestSerializer
    permission_classes = (IsAuthenticated,)
