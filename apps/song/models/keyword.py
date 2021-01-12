from django.db import models


class Keyword(models.Model):
    song = models.ForeignKey('Song',
                             related_name='keywords',
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
