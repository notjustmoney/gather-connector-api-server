from django.db import models


class LikeSong(models.Model):
    song = models.ForeignKey('Song',
                             on_delete=models.CASCADE)
    user = models.ForeignKey('authentication.User',
                             related_name='likes',
                             on_delete=models.CASCADE)
