from django.db import models
from django.utils import timezone

class FAQ(models.Model):
    title = models.CharField(max_length=200, verbose_name="질문")
    content = models.TextField(verbose_name="답변")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "자주 묻는 질문"
        verbose_name_plural = "자주 묻는 질문들"
        

class Notice(models.Model):
    title = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    posted_on = models.DateTimeField(default=timezone.now, verbose_name="게시 날짜")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "공지사항"
        verbose_name_plural = "공지사항들"
        
class CardNews(models.Model):
    title = models.CharField(max_length=200, verbose_name="제목")
    image = models.ImageField(upload_to='cardnews_images/', verbose_name="이미지")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "카드뉴스"
        verbose_name_plural = "카드뉴스들"