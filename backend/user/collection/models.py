from django.conf import settings
from django.db import models


class Collection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    arxiv_entries = models.ManyToManyField('pub.ArxivEntry', through='CollectionArxivEntry')
    github_repos = models.ManyToManyField('pub.GithubRepo', through='CollectionGithubRepo')

    class Meta:
        unique_together = ('user', 'name')


class CollectionItem(models.Model):
    ITEM_TYPES = [
        ('arxiv', 'ArXiv Paper'),
        ('github', 'GitHub Repository'),
    ]

    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES)
    item_id = models.CharField(max_length=100)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('collection', 'item_type', 'item_id')


class CollectionArxivEntry(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    entry = models.ForeignKey('pub.ArxivEntry', on_delete=models.CASCADE)
    collection_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('collection', 'entry')


class CollectionGithubRepo(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    repo = models.ForeignKey('pub.GithubRepo', on_delete=models.CASCADE)
    collection_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('collection', 'repo')
