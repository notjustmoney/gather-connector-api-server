from django.db import models


class Question(models.Model):
    contents = models.TextField()
    is_required = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.contents


class Answer(models.Model):
    user = models.ForeignKey('authentication.User',
                             related_name='answers',
                             on_delete=models.CASCADE)
    question = models.ForeignKey('introduction.Question',
                                 related_name='answers',
                                 on_delete=models.CASCADE)
    contents = models.TextField()
    answered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.contents


