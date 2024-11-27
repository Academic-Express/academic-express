from rest_framework import serializers

from .models import ScholarSubscription, TopicSubscription


class TopicSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicSubscription
        fields = ['id', 'topic', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ScholarSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScholarSubscription
        fields = ['id', 'scholar_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
