from rest_framework import serializers
from pub.serializers import ArxivEntrySerializer, GithubRepoSerializer
from .models import History


class HistorySerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(read_only=True)
    entry_data = serializers.SerializerMethodField()

    class Meta:
        model = History
        fields = ['id', 'content_type', 'viewed_at', 'entry_data']
        read_only_fields = ['viewed_at']

    def get_entry_data(self, obj):
        if obj.arxiv_entry:
            return ArxivEntrySerializer(obj.arxiv_entry).data
        elif obj.github_repo:
            return GithubRepoSerializer(obj.github_repo).data
        return None

    def create(self, validated_data):
        content_type = self.context.get('content_type')
        entry = self.context.get('entry')
        
        if not content_type or not entry:
            raise serializers.ValidationError(
                "content_type and entry are required")

        history_data = {}
        
        match content_type:
            case 'arxiv':
                history_data['arxiv_entry'] = entry
            case 'github':
                history_data['github_repo'] = entry
        
        # 检查是否存在相同的记录
        existing = History.objects.filter(user=validated_data['user'], **history_data).first()

        if existing:
            # 如果存在，只更新访问时间
            existing.save()  # 触发 auto_now
            return existing

        # 如果不存在，创建新记录
        validated_data.update(history_data)
        return super().create(validated_data)
    