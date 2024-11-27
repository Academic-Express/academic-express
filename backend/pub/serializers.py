from rest_framework import serializers

from .models import ArxivEntry, GithubRepo, Collection


class ArxivEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArxivEntry
        exclude = ['synced']


class GithubRepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GithubRepo
        exclude = ['synced']


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'user', 'arxiv_entry', 'github_repo', 'created_at']
        read_only_fields = ['user', 'created_at']
