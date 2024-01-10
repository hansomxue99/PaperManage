from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager


class PaperInfo(models.Model):
    title = models.CharField(max_length=100)  # 文章标题
    author = models.CharField(max_length=100, blank=True)
    paper_author = models.CharField(max_length=100)  # 文章的作者/团队
    source = models.CharField(max_length=100)  # 文章的来源：期刊or会议
    reference = models.CharField(max_length=500, blank=True)  # 参考文献
    pdf_file = models.FileField(upload_to='pdfFiles/%Y%m%d/', blank=True)  # pdf
    tags = TaggableManager(blank=True)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title
