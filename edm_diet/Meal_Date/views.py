from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Meal_Date
from .serializers import MealSerializer

# 뷰 아이템 생성
class MealViewSet(viewsets.ModelViewSet):
    qureyset = Meal_Date.objects.all()
    serializer_class = MealSerializer
    
def auto_save_meal(self, user, food, meal_type, registration_time):
        
        new_data = Meal_Date(user_uid = user, food_name = food, )

# @api_view(['GET'])
# def getTestDatas(request):
#     datas = 