from django.db import models


class Song(models.Model):
    title = models.CharField(max_length=100)
    uri = models.URLField(unique=True)
    play_cnt = models.IntegerField(default=0)
    like_cnt = models.IntegerField(default=0, null=False, blank=True)

    def __str__(self):
        return f"{self.title}"
