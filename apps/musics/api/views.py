from django.shortcuts import get_object_or_404

from rest_framework import exceptions, generics, status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from ..models import Song, Keyword, SongRequest, Comment, LikeSong, LikeComment

from .permissions import IsOwnerOrReadOnly
from .serializers import (LikeSongSerializer, LikeCommentSerializer,
                          KeywordSerializer, SongSerializer, SongRequestSerializer,
                          SongRequestCommentSerializer, SongCommentSerializer)


class SongViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class SongRequestViewSet(viewsets.ModelViewSet):
    queryset = SongRequest.objects.all()
    serializer_class = SongRequestSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MySongRequestListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = SongRequest.objects.all()
    serializer_class = SongRequestSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return SongRequest.objects.filter(user=user)


class SongRequestCommentViewSet(viewsets.ModelViewSet):
    lookup_url_kwarg = 'comment_id'
    queryset = Comment.objects.all()
    serializer_class = SongRequestCommentSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        user = self.request.user
        song_request_id = self.kwargs.get('song_request_id', None)
        song_request = get_object_or_404(SongRequest, pk=song_request_id)
        serializer.save(user=user, song_request=song_request)


class SongRequestCommentListAPIView(generics.ListCreateAPIView):
    lookup_url_kwarg = 'song_request_id'
    queryset = Comment.objects.all()
    serializer_class = SongRequestCommentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        song_request_id = self.kwargs.get('song_request_id', None)
        song_request = get_object_or_404(SongRequest, pk=song_request_id)
        serializer.save(user=user, song_request=song_request)


class SongRequestCommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_fields = ['song_request_id', 'comment_id']
    lookup_url_kwarg = 'comment_id'
    queryset = Comment.objects.all()
    serializer_class = SongRequestCommentSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)


class SongCommentListAPIView(generics.ListCreateAPIView):
    lookup_fields = ['song_id']
    queryset = Comment.objects.all()
    serializer_class = SongCommentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        song_id = self.kwargs.get('song_id', None)
        song = get_object_or_404(Song, pk=song_id)
        serializer.save(user=user, song=song)


class SongCommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    # lookup_field = 'comment_id'
    lookup_url_kwarg = 'comment_id'
    queryset = Comment.objects.all()
    serializer_class = SongCommentSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)


class SongLikeAPIView(generics.CreateAPIView):
    queryset = LikeSong.objects.all()
    serializer_class = LikeSongSerializer
    permission_classes = (IsAuthenticated,)

    def get_song(self):
        song_id = self.kwargs.get('pk', None)
        return get_object_or_404(Song, pk=song_id)

    def get_song_request(self):
        song_request_id = self.kwargs.get('pk', None)
        return get_object_or_404(SongRequest, pk=song_request_id)

    def perform_create(self, serializer):
        user = self.request.user

        url_path = self.request.get_full_path()
        if 'playlist' in url_path:
            song_request = self.get_song_request()
            song = song_request.song
        else:
            song = self.get_song()

        try:
            like = LikeSong.objects.get(user=user, song=song)
            song.like_cnt -= 1
            song.save()
            like.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except LikeSong.DoesNotExist:
            song.like_cnt += 1
            song.save()
            serializer.save(user=user, song=song)


class CommentLikeAPIView(generics.CreateAPIView):
    lookup_url_kwarg = 'comment_id'
    queryset = LikeComment.objects.all()
    serializer_class = LikeCommentSerializer
    permission_classes = (IsAuthenticated,)

    def get_comment(self):
        comment_id = self.kwargs.get('comment_id', None)
        return get_object_or_404(Comment, pk=comment_id)

    def perform_create(self, serializer):
        user = self.request.user
        comment = self.get_comment()
        try:
            like = LikeComment.objects.get(user=user, comment=comment)
            comment.like_cnt -= 1
            comment.save()
            like.delete()
        except LikeComment.DoesNotExist:
            comment.like_cnt += 1
            comment.save()
            serializer.save(user=user, comment=comment)

