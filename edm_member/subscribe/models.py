from django.db import models
from user.models import User

class SubscribeManager(models.Manager):
    pass

class Subscribe(models.Model):
    subscribe_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_subscribe',to_field="uuid")
    subscribe_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_subscribe',to_field="uuid")
    created_at = models.DateTimeField(editable=False,auto_now_add=True)
    
    # 매니저
    objects = SubscribeManager()