from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    """
    网站用户。
    """

    nickname = models.CharField(max_length=255, verbose_name='昵称')
    phone = models.CharField(max_length=32, verbose_name='手机号')
    url = models.URLField(max_length=255, verbose_name='个人主页', blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
