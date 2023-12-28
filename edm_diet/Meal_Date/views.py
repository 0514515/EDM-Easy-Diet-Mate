from django.shortcuts import render
from django.http import Http404, HttpRequest
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Usermeal
from .models import Nutrient
from .serializers import MealSerializer, NutrientSerializer 
from datetime import datetime

import requests

# 뷰 아이템 생성
class Mealviewset(viewsets.ModelViewSet):
    queryset = Usermeal.objects.all()
    serializer_class = MealSerializer
    
    @action(detail=False, methods=['post'])
    
    def save_meal(self, request):
        serializer = MealSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class Nutrientviewset(viewsets.ModelViewSet):
    queryset = Nutrient.objects.all()
    serializer_class = NutrientSerializer 
  
               
def get_user_data(user_api):
    user_uuid,
    user_info,
    

def display_user_meal_evaluation(request):
    # 여기서 user_uid와 meal_id를 가져와서 evaluate_user_meal 함수 호출
    user_uid = '1' 
    meal_time = '2023-12-27'  
    print('1번 함수 작동')
    
    diet_rating = evaluate_user_meal(user_uid, meal_time)

    # 템플릿 렌더링
    return render(request, 'user_meal_evaluation.html', {'diet_rating': diet_rating})
        
        
def get_user_meal(user_uid, meal_time):
    # 사용자의 uid와 time을 기준으로 음식 이름을 가져옴
    user_meals= Usermeal.objects.filter(user_id = user_uid, created_at = meal_time) 
    
    # 가져올 음식에 대한 처리
    meal_nutrient = []
    for user_meal in user_meals:
        food = user_meal.food_name
        total = get_nutrient(food)
        meal_nutrient.append(total)
    # print(meal_nutrient)
    carbs = sum_nutrients(meal_nutrient, 'carbs') # 탄
    prot = sum_nutrients(meal_nutrient, 'protein') # 단
    fat = sum_nutrients(meal_nutrient, 'fat') # 지
    sugar = sum_nutrients(meal_nutrient, 'sugar') # 당
    
    return (carbs, prot, fat, sugar)
    
def sum_nutrients(meal_nutrient, nutrient_key):
    return sum(item[nutrient_key] for item in meal_nutrient) # 하루에 대한 탄,단,지,당 등을 더하는 함수

def get_nutrient(food_name):
    try:
        nutrient = Nutrient.objects.get(food_name = food_name)
        return {
            'carbs': nutrient.carbs_g,
            'protein': nutrient.protein_g,
            'fat': nutrient.fat_g,
            'sugar': nutrient.sugar_g, 
        }
    except Usermeal.DoesNotExist:
        raise Http404("Usermeal does not exist")        


def evaluate_user_meal(user_uid, meal_time):
    # 사용자의 권장 섭취량 계산
    print('2번 함수 작동')
    user_data = (170, 70, '2000-09-27', '남자', 3, 'loss')
    recommend_nutrients = calculate(*user_data)
    # print(recommend_nutrients)
    # 사용자의 DB에서 저장된 식사 데이터 가져오기
    user_meal_nut = get_user_meal(user_uid, meal_time)
    print(user_meal_nut)
    # evaluate 함수를 사용하여 평가 수행
    diet_rating = evaluate(user_meal_nut, recommend_nutrients)
    return diet_rating

       
        
def calculate_age(birth_date):
    print('4번 함수 작동')
    today = datetime.now()
    birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
    age = today.year - birth_date.year - \
        ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


def calcuate_protein(weight, activity_level):
    print('5번 함수 작동')
    protein_factors = {
        1: (0.8, 0.9),
        2: (1.0, 1.2),
        3: (1.2, 1.5),
        4: (1.5, 1.8),
        5: (2.0, 2.0)
    }

    min_factor, max_factor = protein_factors.get(activity_level, (0, 0))
    min_protein = weight * min_factor * 4
    max_protein = weight * max_factor * 4

    return min_protein, max_protein


def calculate(height, weight, birth_date, sex, activity_level, goal):
    # 나이
    age = calculate_age(birth_date)

    # 1. 기초대사량
    if sex == '남자':
        base_rate = 66.47 + (13.75 * (weight-10) + (5 * height) - (6.76 * age))
    else:
        base_rate = 65.51 + (9.56 * (weight-10) +
                             (1.85 * height) - (4.68 * age))

    # 활동 레벨 따라
    activity_factors = {1: 0.1, 2: 0.2, 3: 0.375, 4: 0.5, 5: 0.725}
    activity_rate = base_rate * activity_factors.get(activity_level, 0)

    # 식단 목적 따라
    goal_factors = {'loss': -200, 'stay': 0, 'gain': 200}
    tdee = base_rate + activity_rate + goal_factors.get(goal, 0)

    if sex == '남자' and tdee < 1500:
        tdee = 1500
    elif sex == '여자' and tdee < 1000:
        tdee = 1000

    # 2. 단백질 protein - 지방 fat - 탄수화물 carbs 식 - 당류 sugar.?
    # 일단 전부 kcal 결과
    protein = calcuate_protein(weight, activity_level)
    fat = tdee * 0.2 / 9
    carbs = ((tdee - (protein[0] + fat * 9)) / 4,
             (tdee - (protein[1] + fat * 9)) / 4)
    sugar = tdee * 0.1 / 4

    recommend = {
        'age': int(age),
        'protein': protein,
        'fat': fat,
        'carbs': (carbs[0], carbs[1]),
        'sugar': sugar
    }

    return recommend

# 식단 평가 : Perfect, Very Good, Good, Not Bad, Bad

def evaluate(user_meal, recommend):
    print('6번 함수 작동')
    print(user_meal)
    print(recommend)
    def calculate_error(recommend, actual):
        print('7번 함수 작동')
        print(f"Recommend: {recommend}, Actual: {actual}")
        if isinstance(recommend, tuple):
            # 튜플 형태의 권장 섭취량에 대한 오차 계산
            min_error = abs((actual - recommend[0])) / recommend[0] * 100
            max_error = abs((actual - recommend[1])) / recommend[1] * 100
            return min(min_error, max_error)
        else:
            # 단일 값 형태의 권장 섭취량에 대한 오차 계산
            return abs((actual - recommend)) / recommend * 100  
    
    carbs_error = calculate_error(recommend['carbs'], user_meal[0])
    protein_error = calculate_error(recommend['protein'], user_meal[1])
    fat_error = calculate_error(recommend['fat'], user_meal[2])

    errors = [carbs_error, protein_error, fat_error]
    max_error = max(errors)

    print(f"Errors : carbs={carbs_error}, protein={protein_error}, fat={fat_error}, max_errror={max_error}")
    
    if all(error <= 10 for error in errors):
        return 'perfect'
    elif all(error <= 15 for error in errors):
        return 'very good'
    elif all(error <= 20 for error in errors):
        return 'good'
    elif all(error <= 25 for error in errors):
        return 'not bad'
    elif max_error >= 40 or any(error > 30 for error in errors):
        return 'bad'
    else:
        return 'not bad'


user_data = (170, 70, '2000-09-27', '남자', 3, 'loss')
recommend_nutrients = calculate(*user_data)

# 사용자 실제 식단 데이터 예시
# user_meal = {
#     'carbs': 350,
#     'protein': 400,
#     'fat': 45,
#     'sugar': 300,
# }

request = HttpRequest()
user_meal = display_user_meal_evaluation(request)



#diet_rating = evaluate(user_meal, recommend_nutrients)
#print("Result: ", diet_rating)