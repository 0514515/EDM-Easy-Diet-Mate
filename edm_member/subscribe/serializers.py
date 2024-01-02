from rest_framework import serializers
from .models import Subscribe
from user.models import User

class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ['subscribe_from','subscribe_to']
        
        
class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name']