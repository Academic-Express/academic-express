from django.db import models
from django.utils.text import slugify

from .utils import normalize_author

# Create your models here.


class ArxivEntryAuthor(models.Model):
    """
    ArXiv 论文作者。
    """
    arxiv_entry = models.ForeignKey('ArxivEntry', on_delete=models.CASCADE, verbose_name='ArXiv 论文')
    first_name = models.CharField(max_length=255, verbose_name='名')
    middle_name = models.CharField(max_length=255, verbose_name='中间名', null=True)
    last_name = models.CharField(max_length=255, verbose_name='姓')
    affiliation = models.CharField(max_length=255, verbose_name='机构', null=True)

    class Meta:
        verbose_name = 'ArXiv 论文作者'
        verbose_name_plural = 'ArXiv 论文作者'
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
        ]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class ArxivEntry(models.Model):
    """
    ArXiv 论文。
    """
    arxiv_id = models.CharField(max_length=255, primary_key=True, verbose_name='ArXiv ID')
    title = models.TextField(verbose_name='标题')
    summary = models.TextField(verbose_name='摘要')
    authors = models.JSONField(verbose_name='作者')
    comment = models.TextField(verbose_name='评论', null=True)
    published = models.DateTimeField(verbose_name='发布时间')
    updated = models.DateTimeField(verbose_name='更新时间')
    primary_category = models.CharField(max_length=255, verbose_name='主要类别')
    categories = models.JSONField(verbose_name='所有类别')
    link = models.URLField(max_length=255, verbose_name='ArXiv 链接')
    pdf = models.URLField(max_length=255, verbose_name='PDF 链接')

    slug = models.SlugField(max_length=255, blank=True, verbose_name='Slug')

    view_count = models.IntegerField(default=0, verbose_name='浏览次数')
    citation_count = models.IntegerField(default=0, verbose_name='引用次数')

    synced = models.BooleanField(default=False, verbose_name='已同步')

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

    def make_authors(self) -> list[ArxivEntryAuthor]:
        author_instances = []
        for author in self.authors:
            normalized = normalize_author(author["name"], author.get("affiliation"))
            instance = ArxivEntryAuthor(arxiv_entry=self, **normalized)
            author_instances.append(instance)
        return author_instances


class ArxivCategory(models.Model):
    """
    ArXiv 分类。
    """
    category_id = models.CharField(max_length=255, primary_key=True, verbose_name='分类 ID')
    name = models.CharField(max_length=255, verbose_name='名称')
    description = models.TextField(verbose_name='描述')

    class Meta:
        verbose_name = 'ArXiv 分类'
        verbose_name_plural = 'ArXiv 分类'

    def __str__(self):
        return self.name


class GithubRepo(models.Model):
    """
    GitHub 仓库。
    """
    repo_id = models.CharField(max_length=255, primary_key=True, verbose_name='仓库 ID')
    name = models.CharField(max_length=255, verbose_name='名称')
    full_name = models.CharField(max_length=255, verbose_name='全名')
    description = models.TextField(verbose_name='描述', null=True)
    html_url = models.URLField(max_length=255, verbose_name='链接')
    owner = models.JSONField(verbose_name='所有者')

    created_at = models.DateTimeField(verbose_name='创建时间')
    updated_at = models.DateTimeField(verbose_name='更新时间')
    pushed_at = models.DateTimeField(verbose_name='推送时间')

    homepage = models.URLField(max_length=255, verbose_name='主页', null=True)
    size = models.IntegerField(default=0, verbose_name='大小')
    language = models.CharField(max_length=255, verbose_name='语言', null=True)
    license = models.CharField(max_length=255, verbose_name='许可', null=True)
    topics = models.JSONField(verbose_name='主题')

    stargazers_count = models.IntegerField(default=0, verbose_name='Star 数量')
    forks_count = models.IntegerField(default=0, verbose_name='Fork 数量')
    open_issues_count = models.IntegerField(default=0, verbose_name='开放 Issue 数量')
    network_count = models.IntegerField(default=0, verbose_name='网络数量')
    subscribers_count = models.IntegerField(default=0, verbose_name='Watch 数量')

    readme = models.TextField(verbose_name='README', null=True, blank=True)

    view_count = models.IntegerField(default=0, verbose_name='浏览次数')

    synced = models.BooleanField(default=False, verbose_name='已同步')

    class Meta:
        verbose_name = 'GitHub 仓库'
        verbose_name_plural = 'GitHub 仓库'

    def __str__(self):
        return self.full_name
