from rest_framework import serializers
from .models import Usermeal, Nutrient, Usermealevaluation


class MealSerializer(serializers.ModelSerializer):   
     class Meta:
        model = Usermeal
        fields = '__all__'    

class NutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrient
        fieds = '__all__'

class UsermealevaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usermealevaluation
        fieds = '__all__'