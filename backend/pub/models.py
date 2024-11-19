from django.db import models
from django.utils.text import slugify

# Create your models here.


class ArxivEntry(models.Model):
    """
    ArXiv 论文。
    """
    arxiv_id = models.CharField(max_length=255, primary_key=True, verbose_name='ArXiv ID')
    title = models.TextField(verbose_name='标题')
    summary = models.TextField(verbose_name='摘要')
    authors = models.JSONField(verbose_name='作者')
    comment = models.TextField(verbose_name='评论', blank=True)
    published = models.DateTimeField(verbose_name='发布时间')
    updated = models.DateTimeField(verbose_name='更新时间')
    primary_category = models.CharField(max_length=255, verbose_name='主要类别')
    categories = models.JSONField(verbose_name='所有类别')
    link = models.URLField(max_length=255, verbose_name='ArXiv 链接')
    pdf = models.URLField(max_length=255, verbose_name='PDF 链接')

    slug = models.SlugField(max_length=255, blank=True, verbose_name='Slug')

    view_count = models.IntegerField(default=0, verbose_name='浏览次数')
    citation_count = models.IntegerField(default=0, verbose_name='引用次数')

    class Meta:
        verbose_name = 'ArXiv 论文'
        verbose_name_plural = 'ArXiv 论文'

    def __str__(self):
        return f'[{self.arxiv_id}] {self.title}'

    def save(self, *args, **kwargs):
        self.make_slug()
        super().save(*args, **kwargs)

    def make_slug(self):
        if not self.slug:
            self.slug = slugify(self.title)
