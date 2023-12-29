from rest_framework import serializers
from .models import FAQ, Notice, CardNews


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'


class CardNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardNews
        fields = '__all__'