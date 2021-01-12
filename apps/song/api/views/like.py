from rest_framework import status
from rest_framework.response import Response

from apps.song.models import LikeComment, LikeSong

from ..serializers import LikeCommentSerializer, LikeSongSerializer


def like_song(request, user, song):
    try:
        like = LikeSong.objects.get(user=user, song=song)
        song.like_cnt -= 1
        song.save()
        like.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    except LikeSong.DoesNotExist:
        song.like_cnt += 1
        song.save()

        serializer = LikeSongSerializer(data={}, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user, song=song)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def like_comment(request, user, comment):
    try:
        like = LikeComment.objects.get(user=user, comment=comment)
        comment.like_cnt -= 1
        comment.save()
        like.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    except LikeComment.DoesNotExist:
        comment.like_cnt += 1
        comment.save()

        serializer = LikeCommentSerializer(data={}, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user, comment=comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
