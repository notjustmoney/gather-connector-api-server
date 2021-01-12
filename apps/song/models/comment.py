from django.db import models


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
