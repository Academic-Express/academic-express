from rest_framework import serializers

from comment.models import Comment, Vote
from user.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    vote_count = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'resource', 'content', 'author', 'parent',
                  'created_at', 'updated_at', 'vote_count', 'user_vote', 'replies']
        read_only_fields = ['author', 'resource']

    def get_vote_count(self, obj):
        return sum(vote.value for vote in obj.votes.all())

    def get_user_vote(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                vote = obj.votes.get(user=request.user)
                return vote.value
            except Vote.DoesNotExist:
                pass
        return 0

    def get_replies(self, obj):
        if obj.parent is None:  # Only get replies for top-level comments
            replies = Comment.objects.filter(parent=obj)
            return CommentSerializer(replies, many=True, context=self.context).data
        return []

    def to_representation(self, instance):
        # 确保单个对象返回时不是列表
        ret = super().to_representation(instance)
        return ret


class VoteSerializer(serializers.Serializer):
    value = serializers.IntegerField()

    def validate_value(self, value):
        if value not in [Comment.VOTE_UP, Comment.VOTE_DOWN]:
            raise serializers.ValidationError("Invalid vote value")
        return value
