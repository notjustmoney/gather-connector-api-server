from django.db import models


class SongRequest(models.Model):
    song = models.ForeignKey('Song',
                             related_name='song_requests',
                             related_query_name='song',
                             on_delete=models.CASCADE)
    user = models.ForeignKey('authentication.User',
                             related_name='song_requests',
                             on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    played_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
