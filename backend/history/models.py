from django.conf import settings
from django.db import models


class History(models.Model):
    """浏览历史记录"""

    def __str__(self):
        if self.arxiv_entry:
            return f"arxiv:{self.arxiv_entry.arxiv_id}"
        elif self.github_repo:
            return f"github:{self.github_repo.repo_id}"
        return "deleted entry"

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now=True)
    
    # 外键关联
    arxiv_entry = models.ForeignKey('pub.ArxivEntry', 
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True)
    github_repo = models.ForeignKey('pub.GithubRepo',
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True)

    class Meta:
        ordering = ['-viewed_at']
        verbose_name_plural = 'histories'

    @property
    def content_type(self):
        """动态判断内容类型"""
        if self.arxiv_entry:
            return 'arxiv'
        elif self.github_repo:
            return 'github'
        return None
