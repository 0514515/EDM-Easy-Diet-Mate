from rest_framework import serializers
from .models import Subscribe
from user.models import User

# 구독 조회, 생성, 삭제용 Serializer
class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ['subscribe_from','subscribe_to']
        
# 구독 1명의 이름 조회용 Serializer
class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name']