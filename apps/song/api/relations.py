from rest_framework import serializers
from rest_framework.reverse import reverse


class CommentHyperlinkField(serializers.HyperlinkedIdentityField):
    # We define these as class attributes, so we don't need to pass them as arguments.
    view_name = 'song-comments-list'

    def get_url(self, obj, view_name, request, format=None):
        url_kwargs = {
            'song_pk': obj.song.id,
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
            'song_pk': view_kwargs['song_pk']
        }
        return self.get_queryset().get(**lookup_kwargs)
