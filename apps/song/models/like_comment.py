from django.db import models


class LikeComment(models.Model):
    comment = models.ForeignKey('Comment',
                                related_name='likes',
                                on_delete=models.CASCADE)
    user = models.ForeignKey('authentication.User',
                             on_delete=models.CASCADE)
