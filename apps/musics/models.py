from django.db import models


class Keyword(models.Model):
    song = models.ForeignKey('Song',
                             related_name='keywords',
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    # cnt = models.IntegerField(default=0, blank=True)


class Song(models.Model):
    title = models.CharField(max_length=100)
    uri = models.URLField(unique=True)
    play_cnt = models.IntegerField(default=0)
    like_cnt = models.IntegerField(default=0, null=False, blank=True)

    def __str__(self):
        return f"{self.title}"


class SongRequest(models.Model):
    song = models.ForeignKey('Song',
                             related_name='song_requests',
                             related_query_name='song',
                             on_delete=models.CASCADE)
    user = models.ForeignKey('authentication.User',
                             related_name='song_requests',
                             on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    played_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


class LikeSong(models.Model):
    song = models.ForeignKey('Song',
                             on_delete=models.CASCADE)
    user = models.ForeignKey('authentication.User',
                             related_name='likes',
                             on_delete=models.CASCADE)


class LikeComment(models.Model):
    comment = models.ForeignKey('Comment',
                                related_name='likes',
                                on_delete=models.CASCADE)
    user = models.ForeignKey('authentication.User',
                             on_delete=models.CASCADE)


class Comment(models.Model):
    song = models.ForeignKey('Song', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey('authentication.User', related_name='comments', on_delete=models.CASCADE)
    contents = models.CharField(max_length=500)
    like_cnt = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.contents} ({self.user})'
