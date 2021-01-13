from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from rest_framework import serializers, exceptions

from apps.song.models import SongRequest, Keyword, Song
from apps.common.scrapper import get_video_title_and_uri

from ..relations import CommentHyperlinkField


class SongRequestSerializer(serializers.ModelSerializer):
    data_type = serializers.ChoiceField(['uri', 'keyword'], write_only=True)
    data = serializers.CharField(max_length=50, write_only=True)

    song = serializers.HyperlinkedRelatedField(read_only=True, view_name='song-detail')
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    like_cnt = serializers.ReadOnlyField(source='song.like_cnt')
    play_cnt = serializers.ReadOnlyField(source='song.play_cnt')
    comments = CommentHyperlinkField(view_name='song-comments-list', read_only=True)

    class Meta:
        model = SongRequest
        fields = ['url', 'song', 'user', 'requested_at', 'updated_at', 'played_at', 'data_type', 'data', 'like_cnt', 'play_cnt', 'comments']

    def create(self, validated_data):
        data_type = validated_data.pop('data_type', None)
        data = validated_data.pop('data', None)
        user = validated_data['user']

        if data_type == 'keyword':
            try:
                keyword = Keyword.objects.get(name=data)
                song = keyword.song
            except Keyword.DoesNotExist:
                video_title, video_uri = get_video_title_and_uri(data)
                song, created = Song.objects.get_or_create(title=video_title, uri=video_uri)
                Keyword.objects.get_or_create(song=song, name=data)
        elif data_type == 'uri':
            song, created = Song.objects.get_or_create(uri=data)
        else:
            raise exceptions.NotAcceptable('지원하지 않는 유형입니다.')
        song_request = super().create({"song": song, "user": user})
        return song_request

    def update(self, instance, validated_data):
        data_type = validated_data.pop('data_type', None)
        data = validated_data.pop('data', None)

        if data_type == 'keyword':
            try:
                keyword = Keyword.objects.get(name=data)
                song = keyword.song
            except Keyword.DoesNotExist:
                video_title, video_uri = get_video_title_and_uri(data)
                song, created = Song.objects.get_or_create(title=video_title, uri=video_uri)
                Keyword.objects.get_or_create(song=song, name=data)
        elif data_type == 'uri':
            song, created = Song.objects.get_or_create(uri=data)
        else:
            raise exceptions.NotAcceptable('지원하지 않는 유형입니다.')
        instance.song = song
        instance.save()
        return instance

    def validate(self, attrs):
        data_type = attrs['data_type']

        if data_type == 'uri':
            uri = attrs['data']
            validator = URLValidator()
            try:
                validator(uri)
            except ValidationError:
                raise serializers.ValidationError('wrong uri')
        elif data_type == 'keyword':
            keyword = attrs['data']
            if len(keyword) > 50:
                raise serializers.ValidationError('keyword is too long')
        return attrs
