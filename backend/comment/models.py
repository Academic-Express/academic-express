from django.conf import settings
from django.db import models


class Comment(models.Model):
    VOTE_UP = 1
    VOTE_DOWN = -1
    VOTE_CHOICES = [
        (VOTE_UP, 'Up'),
        (VOTE_DOWN, 'Down'),
    ]

    resource = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class Vote(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=Comment.VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['comment', 'user']
