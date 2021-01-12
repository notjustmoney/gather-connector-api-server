from rest_framework import serializers

from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from apps.song.models import Song, LikeSong, LikeComment, Comment, Keyword

from ..relations import CommentHyperlinkField


class SongCommentSerializer(serializers.ModelSerializer):
    song = serializers.HyperlinkedRelatedField(read_only=True, view_name='song-detail')
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    # url = CommentHyperlink(read_only=True, view_name='song-comments-detail')

    class Meta:
        model = Comment
        fields = ['song', 'user', 'contents', 'created_at', 'updated_at', 'like_cnt']


class SongSerializer(serializers.ModelSerializer):
    comments = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='song-comments-detail',
        parent_lookup_kwargs={'song_pk': 'song__pk'}
    )

    class Meta:
        model = Song
        fields = ['url', 'title', 'play_cnt', 'like_cnt', 'comments']


class LikeSongSerializer(serializers.ModelSerializer):
    song = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='song-detail')
    user = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail')

    class Meta:
        model = LikeSong
        fields = ['song', 'user']


class LikeCommentSerializer(serializers.ModelSerializer):
    comment = NestedHyperlinkedRelatedField(
        read_only=True,
        view_name='song-comments-detail',
        parent_lookup_kwargs={'song_pk': 'song__pk'})
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')

    class Meta:
        model = LikeComment
        fields = ['comment', 'user']


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'
