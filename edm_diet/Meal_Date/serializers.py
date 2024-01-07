from rest_framework import serializers
from .models import *
import uuid

class MealSerializer(serializers.ModelSerializer):
     user_id = serializers.UUIDField(default=uuid.uuid4)   
     class Meta:
        model = Usermeal
        fields = '__all__'    

class NutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrient
        fields = '__all__'

class UsermealevaluationSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(default=uuid.uuid4)
    class Meta:
        model = Usermealevaluation
        fields = '__all__'
        
class ImagesaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagesave
        fields = '__all__'