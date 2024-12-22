from drf_spectacular.utils import (PolymorphicProxySerializer,
                                   extend_schema_field)
from rest_framework import serializers

from user.serializers import UserSerializer

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
    user = UserSerializer()

    class Meta:
        model = ResourceClaim
        fields = ['id', 'user', 'resource_type', 'resource_id', 'created_at']
        read_only_fields = ['created_at']


class UserResourceClaimSerializer(serializers.ModelSerializer):
    resource = serializers.SerializerMethodField()

    class Meta:
        model = ResourceClaim
        fields = ['id', 'user', 'resource_type', 'resource_id', 'created_at', 'resource']
        read_only_fields = ['created_at']

    @extend_schema_field(PolymorphicProxySerializer(
        component_name='ResourceItem',
        serializers=[
            ArxivEntrySerializer,
            GithubRepoSerializer,
        ],
        resource_type_field_name=None,
    ))
    def get_resource(self, obj):
        if obj.resource_type == 'arxiv':
            try:
                entry = ArxivEntry.objects.get(arxiv_id=obj.resource_id)
                return ArxivEntrySerializer(entry).data
            except ArxivEntry.DoesNotExist:
                return None
        elif obj.resource_type == 'github':
            try:
                repo = GithubRepo.objects.get(repo_id=obj.resource_id)
                return GithubRepoSerializer(repo).data
            except GithubRepo.DoesNotExist:
                return None
        return None
