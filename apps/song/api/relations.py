from rest_framework import serializers
from rest_framework.reverse import reverse

from ..models import Comment, LikeComment


class CommentHyperlinkField(serializers.HyperlinkedIdentityField):
    # We define these as class attributes, so we don't need to pass them as arguments.
    view_name = 'comment-detail'

    def get_url(self, obj, view_name, request, format=None):
        if isinstance(obj, LikeComment):
            url_kwargs = {
                'song_id': obj.comment.song.id,
                'comment_id': obj.comment.id,
            }
        elif isinstance(obj, Comment):
            url_kwargs = {
                'song_id': obj.song.id,
                'comment_id': obj.id,
            }
        else:
            print(request.path)
            return request
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
            'song_id': view_kwargs['song_id'],
            'comment_id': view_kwargs['comment_id']
        }
        return self.get_queryset().get(**lookup_kwargs)
