from .serializers import HistorySerializer


def record_history(user, content_type, entry):
    """
    记录用户访问历史

    Args:
        user: 用户对象
        content_type: 'arxiv' 或 'github'
        entry: ArxivEntry 或 GithubRepo 对象
    """
    serializer = HistorySerializer(
        data={},
        context={'content_type': content_type, 'entry': entry}
    )
    if serializer.is_valid():
        serializer.save(user=user)
    return serializer
