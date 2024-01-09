from django.db import models
from user.models import User

class SubscribeManager(models.Manager):
    def create_subscribe(self, from_user, to_user):
        subscribe = self.create(subscribe_from=from_user, subscribe_to=to_user)
        return subscribe

# 구독 모델
class Subscribe(models.Model):
    subscribe_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_subscribe',to_field="uuid")   # 구독하는 유저의 uuid 필드
    subscribe_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_subscribe',to_field="uuid")   # 구독받는 유저의 uuid 필드
    created_at = models.DateTimeField(editable=False,auto_now_add=True)
    
    # 매니저
    objects = SubscribeManager()
    
    class Meta:
        unique_together = [['subscribe_from', 'subscribe_to']]
        verbose_name = "구독"
        verbose_name_plural = "구독 목록"  # 관리자 페이지에서 표시될 목록 제목