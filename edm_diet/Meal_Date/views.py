from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import *
from datetime import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication
import requests
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view,permission_classes

@api_view(['GET'])
@permission_classes([AllowAny])
def display_user_meal_evaluation(request):
    token = validate_token(request)
    if isinstance(token, JsonResponse):
        return token  # validate_token이 Response 객체를 반환한 경우, 해당 응답을 그대로 반환
    
    try:
        user_info = get_user_info(token)
        uuid = str(user_info.get('uuid', '')) 
        meal_date = request.query_params.get('meal_date', '2023-12-29')
        meal_type = request.query_params.get('meal_type', '아침')
        meal_serving = float(request.query_params.get('meal_serving', 1))
        
        # 데이터베이스에서 해당 user_uid에 해당하는 객체 가져오기
        diet_rating = evaluate_user_meal(token, meal_date)
        user_meal_nut = get_user_meal(uuid, meal_date, meal_type)
        
        template_data = {'diet_rating': diet_rating[0], 
                        'total_carbs': diet_rating[1][0], 
                         'total_protein': diet_rating[1][1], 
                         'total_fat': diet_rating[1][2], 
                         'total_sugar': diet_rating[1][3], 
                         'total_kcal' : diet_rating[1][4],
                         'total_nat': diet_rating[1][5], 
                         'total_col': diet_rating[1][6], 
                         'carbs': user_meal_nut[0], 
                         'protein': user_meal_nut[1], 
                         'fat': user_meal_nut[2], 
                         'sugar': user_meal_nut[3], 
                         'kcal' : user_meal_nut[4],
                         'nat': user_meal_nut[5], 
                         'col': user_meal_nut[6]
                         }

        save_user_evaluation(uuid, meal_date, diet_rating[0], diet_rating[1])
        return JsonResponse(template_data, safe=False)
    
    except ObjectDoesNotExist:
        # 데이터베이스에서 해당 user_uid에 해당하는 객체가 없을 때의 예외 처리
        return Response({'error': '정보를 찾을 수 없음'}, status=status.HTTP_404_NOT_FOUND)

def validate_token(request):
    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        return JsonResponse({"message": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)
    
    jwt_authenticator = JWTAuthentication()
    try:
        validated_token = jwt_authenticator.get_validated_token(request.headers.get('Authorization').split(' ')[1])
        return str(validated_token)
    
    except Exception as e:
        return JsonResponse({"message": "Invalid token"}, status=status.HTTP_403_FORBIDDEN)

def get_user_info(token):
    if isinstance(token, JsonResponse):
        return token 
    url = 'http://edm.japaneast.cloudapp.azure.com/api/user/info/'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token, # 실제로 받는 토큰
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            user_info = data.get('user', {})
            user_info['uuid'] = str(user_info.get('uuid', ''))  # uuid를 문자열로 변환
            return user_info

        else:
            return JsonResponse({'error': f"Request failed with status code {response.status_code}"}, status=500)

    except Exception as e:
        return JsonResponse({'error': f"An error occurred: {e}"}, status=500)

def get_user_meal(uuid, meal_time, meal_type):
    user_uid_after = uuid.replace('-','')
    user_meals = Usermeal.objects.filter(uuid=user_uid_after, meal_date=meal_time, meal_type = meal_type).values(
        'meal_serving', 'food_name__carbs_g', 'food_name__protein_g', 'food_name__fat_g', 'food_name__sugar_g', 'food_name__energy_kcal', 'food_name__nat_mg', 'food_name__col_mg',
    )

    meal_nutrient = []

    for user_meal in user_meals:
        print(user_meal, "@@@@@@@@@@@@!!!!!!!!!!!!!!@@@@@@@@@@@@@@@@@")
        total = {
            'carbs': user_meal['food_name__carbs_g'] * user_meal['meal_serving'],
            'protein': user_meal['food_name__protein_g'] * user_meal['meal_serving'],
            'fat': user_meal['food_name__fat_g'] * user_meal['meal_serving'],
            'sugar': user_meal['food_name__sugar_g'] * user_meal['meal_serving'],
            'kcal' : user_meal['food_name__energy_kcal'] * user_meal['meal_serving'],
            'nat' : user_meal['food_name__nat_mg'] * user_meal['meal_serving'],
            'col' : user_meal['food_name__col_mg'] * user_meal['meal_serving']
        }
        meal_nutrient.append(total)

    carbs = sum_nutrients(meal_nutrient, 'carbs')
    prot = sum_nutrients(meal_nutrient, 'protein')
    fat = sum_nutrients(meal_nutrient, 'fat')
    sugar = sum_nutrients(meal_nutrient, 'sugar')
    kcal = sum_nutrients(meal_nutrient, 'kcal')
    nat = sum_nutrients(meal_nutrient, 'nat')
    col = sum_nutrients(meal_nutrient, 'col')
    
    return carbs, prot, fat, sugar, kcal, nat, col

def evaluate_date_meal(uuid, meal_date):
    user_uid_after = uuid.replace('-','')
    user_meals = Usermeal.objects.filter(uuid=user_uid_after, meal_date=meal_date).values(
        'meal_serving', 'food_name__carbs_g', 'food_name__protein_g', 'food_name__fat_g', 'food_name__sugar_g', 'food_name__energy_kcal', 'food_name__nat_mg', 'food_name__col_mg',
    )

    meal_nutrient = []

    for user_meal in user_meals:
        total = {
            'carbs': user_meal['food_name__carbs_g'] * user_meal['meal_serving'],
            'protein': user_meal['food_name__protein_g'] * user_meal['meal_serving'],
            'fat': user_meal['food_name__fat_g'] * user_meal['meal_serving'],
            'sugar': user_meal['food_name__sugar_g'] * user_meal['meal_serving'],
            'kcal' : user_meal['food_name__energy_kcal'] * user_meal['meal_serving'],
            'nat' : user_meal['food_name__nat_mg'] * user_meal['meal_serving'],
            'col' : user_meal['food_name__col_mg'] * user_meal['meal_serving']
        }
        meal_nutrient.append(total)

    carbs = sum_nutrients(meal_nutrient, 'carbs')
    prot = sum_nutrients(meal_nutrient, 'protein')
    fat = sum_nutrients(meal_nutrient, 'fat')
    sugar = sum_nutrients(meal_nutrient, 'sugar')
    kcal = sum_nutrients(meal_nutrient, 'kcal')
    nat = sum_nutrients(meal_nutrient, 'nat')
    col = sum_nutrients(meal_nutrient, 'col')
    
    return carbs, prot, fat, sugar, kcal, nat, col

def sum_nutrients(meal_nutrient, nutrient_key):
    return sum(item[nutrient_key] for item in meal_nutrient)

def evaluate_user_meal(token, meal_time):
    user_info = get_user_info(token)
    
    uuid = user_info.get('uuid', '')
    user_height = user_info.get('height', '')
    user_weight = user_info.get('weight', '')
    user_active_level = int(user_info.get('active_level', '')[0])
    user_birthdate = user_info.get('birthdate', '')
    user_diet_purpose = user_info.get('diet_purpose', '')
    user_gender = user_info.get('gender', '')
    
    user_data = (user_height, user_weight, user_birthdate, user_gender, user_active_level, user_diet_purpose)
    recommend_nutrients = calculate(*user_data)
    
    user_meal_nut = evaluate_date_meal(uuid, meal_time)
    diet_rating = evaluate(user_meal_nut, recommend_nutrients)
    
    return diet_rating, user_meal_nut

def calculate_age(birth_date):
    today = datetime.now()
    birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def calculate_protein(weight, activity_level):
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
    age = calculate_age(birth_date)

    if sex == '남자':
        base_rate = 66.47 + (13.75 * (weight-10) + (5 * height) - (6.76 * age))
    else:
        base_rate = 65.51 + (9.56 * (weight-10) + (1.85 * height) - (4.68 * age))

    activity_factors = {1: 0.1, 2: 0.2, 3: 0.375, 4: 0.5, 5: 0.725}
    activity_rate = base_rate * activity_factors.get(activity_level, 0)

    goal_factors = {'체중 감량': -200, '체중 유지': 0, '체중증량': 200}
    tdee = base_rate + activity_rate + goal_factors.get(goal, 0)

    if sex == '남자' and tdee < 1500:
        tdee = 1500
    elif sex == '여자' and tdee < 1000:
        tdee = 1000

    protein = calculate_protein(weight, activity_level)
    fat = tdee * 0.2 / 9
    carbs = ((tdee - (protein[0] + fat * 9)) / 4, (tdee - (protein[1] + fat * 9)) / 4)
    sugar = tdee * 0.1 / 4

    recommend = {
        'age': int(age),
        'protein': protein,
        'fat': fat,
        'carbs': (carbs[0], carbs[1]),
        'sugar': sugar
    }

    return recommend

def evaluate(user_meal_nut, recommend):
    def calculate_error(recommend, actual):
        if isinstance(recommend, tuple):
            min_error = abs((actual - recommend[0])) / recommend[0] * 100
            max_error = abs((actual - recommend[1])) / recommend[1] * 100
            return min(min_error, max_error)
        else:
            return abs((actual - recommend)) / recommend * 100

    carbs_error = calculate_error(recommend['carbs'], user_meal_nut[0])
    protein_error = calculate_error(recommend['protein'], user_meal_nut[1])
    fat_error = calculate_error(recommend['fat'], user_meal_nut[2])

    errors = [carbs_error, protein_error, fat_error]
    max_error = max(errors)

    if all(error <= 10 for error in errors):
        return 'Perfect'
    elif all(error <= 15 for error in errors):
        return 'Very Good'
    elif all(error <= 20 for error in errors):
        return 'Good'
    elif all(error <= 25 for error in errors):
        return 'Not Bad'
    elif max_error >= 40 or any(error > 30 for error in errors):
        return 'Bad'
    else:
        return 'Not Bad'

    
def save_user_evaluation(uuid, meal_date, diet_rating, user_meal_nut):
    # 이미 저장된 데이터가 있는지 확인
    existing_evaluation = Usermealevaluation.objects.filter(uuid=uuid, meal_date=meal_date)

    if existing_evaluation:
        # 이미 해당 조건을 만족하는 데이터가 있으면 삭제후 생성및 저장
        existing_evaluation.delete()
        
        new_data = Usermealevaluation(
            uuid=uuid,
            meal_date=meal_date,
            sum_carb=user_meal_nut[0],
            sum_sugar=user_meal_nut[3],
            sum_protein=user_meal_nut[1],
            sum_fat=user_meal_nut[2],
            meal_evaluation=diet_rating,
            sum_kcal=user_meal_nut[4],
            sum_nat=user_meal_nut[5],
            sum_col=user_meal_nut[6]
        )
        new_data.save()
        return new_data
    
    else:
        # 조건을 만족하는 데이터가 없으면 새로운 데이터를 생성하고 저장
        new_data = Usermealevaluation(
            uuid=uuid,
            meal_date=meal_date,
            sum_carb=user_meal_nut[0],
            sum_sugar=user_meal_nut[3],
            sum_protein=user_meal_nut[1],
            sum_fat=user_meal_nut[2],
            meal_evaluation=diet_rating,
            sum_kcal=user_meal_nut[4],
            sum_nat=user_meal_nut[5],
            sum_col=user_meal_nut[6]
        )
        new_data.save()
        return new_data
  
