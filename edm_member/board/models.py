from django.db import models
from django.utils import timezone
from django.conf import settings

# FAQ 모델
class FAQ(models.Model):
    title = models.CharField(max_length=200, verbose_name="질문")
    content = models.TextField(verbose_name="답변")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "자주 묻는 질문"
        verbose_name_plural = "자주 묻는 질문 목록"
        

# 공지 모델
class Notice(models.Model):
    title = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    posted_on = models.DateTimeField(default=timezone.now, verbose_name="게시 날짜")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "공지사항"
        verbose_name_plural = "공지사항 목록"

# 카드뉴스 모델        
class CardNews(models.Model):
    title = models.CharField(max_length=200, verbose_name="제목")
    image = models.ImageField(upload_to='cardnews_images/', verbose_name="이미지")
    link = models.URLField(max_length=250, verbose_name="링크",default='')
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "카드뉴스"
        verbose_name_plural = "카드뉴스 목록"

# 1대1 문의 모델   
class Ask(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='asks', verbose_name="회원")
    title = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    image = models.ImageField(upload_to='ask_images/', verbose_name="사진", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="문의 날짜")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "1대1 문의"
        verbose_name_plural = "1대1 문의 목록"

# 1대1 문의 답변 모델       
class Answer(models.Model):
    ask = models.ForeignKey(Ask, on_delete=models.CASCADE, related_name='answers', verbose_name="문의")
    content = models.TextField(verbose_name="답변 내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="답변 날짜")

    def __str__(self):
        return f"{self.ask.title}에 대한 답변"

    class Meta:
        verbose_name = "답변"
        verbose_name_plural = "답변 목록"