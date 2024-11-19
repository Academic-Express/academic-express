from rest_framework import serializers

from .models import ArxivEntry


class ArxivEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArxivEntry
        fields = '__all__'
