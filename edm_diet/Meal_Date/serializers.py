from rest_framework import serializers
from .models import Meal_Date

# class MealSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Meal_Date
#         fields = ("__all__")


class MealSerializer(serializers.ModelSerializer):   
    def create(self, validated_data):
        meal = Meal_Date.objects.create_     