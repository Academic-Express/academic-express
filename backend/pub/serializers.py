from rest_framework import serializers

from .models import ArxivEntry, GithubRepo, ResourceClaim


class ArxivEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArxivEntry
        exclude = ['synced']


class GithubRepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GithubRepo
        exclude = ['synced']


class ResourceClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceClaim
        fields = ['user', 'resource_type', 'resource_id', 'created_at']
        read_only_fields = ['created_at']
