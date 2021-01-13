import datetime

from django.db.models import Count, Max

from rest_framework import viewsets, exceptions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.song.models import SongRequest, Song
from ..serializers import SongSerializer


class StatisticViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SongRequest.objects.filter(played_at__isnull=False, deleted_at__isnull=True)
    serializer_class = SongSerializer
    # permission_classes =

    def list(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(request.method)

    def retrieve(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(request.method)

    @action(detail=False, methods=['get'])
    def weekly(self, request):
        current_week = datetime.date.today().isocalendar()[0]
        filtered_requests = self.get_queryset().filter(played_at__week=current_week)
        songs = Song.objects.filter(id__in=filtered_requests.values('song_id')).annotate(max_play=Max('play_cnt')).order_by('-max_play')
        if len(songs) == 0:
            raise exceptions.NotFound('신청곡 재생기록을 찾을 수 없습니다.')
        song = songs[0]
        serializer = self.get_serializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def monthly(self, request):
        today = datetime.date.today()
        filtered_requests = self.get_queryset().filter(played_at__month=today.month)
        songs = Song.objects.filter(id__in=filtered_requests.values('song_id')).annotate(max_play=Max('play_cnt')).order_by('-max_play')
        if len(songs) == 0:
            raise exceptions.NotFound('신청곡 재생기록을 찾을 수 없습니다.')
        song = songs[0]
        serializer = self.get_serializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def yearly(self, request):
        today = datetime.date.today()
        filtered_requests = self.get_queryset().filter(played_at__year=today.year)
        songs = Song.objects.filter(id__in=filtered_requests.values('song_id')).annotate(
            max_play=Max('play_cnt')).order_by('-max_play')
        if len(songs) == 0:
            raise exceptions.NotFound('신청곡 재생기록을 찾을 수 없습니다.')
        song = songs[0]
        serializer = self.get_serializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)
