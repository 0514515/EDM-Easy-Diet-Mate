from rest_framework import serializers
from .models import *

# FAQ Serializer
class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

# 공지 Serializer
class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'

# 카드뉴스 Serializer
class CardNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardNews
        fields = '__all__'
 
# 1대1 문의 답변 Serializer       
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'content', 'created_at']
      
# 1대1 문의 Serializer          
class AskSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    class Meta:
        model = Ask
        fields = ['id', 'title', 'content', 'image', 'created_at','answers']
        
