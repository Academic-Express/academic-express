from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


class TopicSubscription(models.Model):
    """
    用户对话题的订阅关系。
    """
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='订阅者')
    topic = models.CharField(max_length=255, verbose_name='话题')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '话题订阅'
        verbose_name_plural = '话题订阅'
        unique_together = ['subscriber', 'topic']

    def __str__(self):
        return f'{self.subscriber} 订阅了话题 {self.topic}'


class ScholarSubscription(models.Model):
    """
    用户对学者的订阅关系。
    """
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='订阅者')
    scholar_name = models.CharField(max_length=255, verbose_name='学者姓名')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '学者订阅'
        verbose_name_plural = '学者订阅'
        unique_together = ['subscriber', 'scholar_name']

    def __str__(self):
        return f'{self.subscriber} 订阅了学者 {self.scholar_name}'
