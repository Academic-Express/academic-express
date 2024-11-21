from rest_framework import serializers

from .models import ArxivEntry, GithubRepo


class ArxivEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArxivEntry
        fields = '__all__'


class GithubRepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GithubRepo
        fields = '__all__'
