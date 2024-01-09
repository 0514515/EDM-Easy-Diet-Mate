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
def display_user_meal_evaluation(request): # 사용자의 하루 식단에 대한 평가와 한 끼 식사에 대한 정보들을 반환해 주는 함수
    token = validate_token(request)
    if isinstance(token, JsonResponse):
        return token  # validate_token이 Response 객체를 반환한 경우, 해당 응답을 그대로 반환
    
    try:
        user_info = get_user_info(token)
        uuid = str(user_info.get('uuid', '')) 
        meal_date = request.query_params.get('meal_date', '2023-12-29') # 날짜 정보를 파라미터에 받아온다 
        meal_type = request.query_params.get('meal_type', '아침') # 식사 타입의 정보를 파라미터에 받아온다

        # 데이터베이스에서 해당 user_uid에 해당하는 객체 가져오기
        diet_rating = evaluate_user_meal(token, meal_date) # 하루 식단에 대한 평가 및 정보
        user_meal_nut = get_user_meal(uuid, meal_date, meal_type) # 한끼 식사에 대한 식사 정보
        
        template_data = {
                        'diet_rating': diet_rating[0], 
                        'total_carbs': diet_rating[1][0], 
                         'total_protein': diet_rating[1][1], 
                         'total_fat': diet_rating[1][2], 
                         'total_sugar': diet_rating[1][3], 
                         'total_kcal' : diet_rating[1][4],
                         'total_nat': diet_rating[1][5], 
                         'total_col': diet_rating[1][6],
                         'imagelink': user_meal_nut[7],
                         'carbs': user_meal_nut[0], 
                         'protein': user_meal_nut[1], 
                         'fat': user_meal_nut[2], 
                         'sugar': user_meal_nut[3], 
                         'kcal' : user_meal_nut[4],
                         'nat': user_meal_nut[5], 
                         'col': user_meal_nut[6],
                         'food_name': user_meal_nut[8],
                         'meal_serving': user_meal_nut[9],
                         "un_food_name" : user_meal_nut[10]
                         }
        
        
        
        save_user_evaluation(uuid, meal_date, diet_rating[0], diet_rating[1]) # 식단 평가한 데이터를 Usermealevaluation 에 저장
        return JsonResponse(template_data, safe=False) # 하루에 대한 평가 및 정보, 한끼 식사 의 성보를 반환 
    
    except ObjectDoesNotExist:
        # 데이터베이스에서 해당 user_uid에 해당하는 객체가 없을 때의 예외 처리
        return Response({'error': '유저 정보를 찾을 수 없음'}, status=status.HTTP_404_NOT_FOUND)

def validate_token(request):
    authorization_header = request.headers.get('Authorization') # header 에서 'Authorization'에서 사용자의 토큰을 받아옴
    if not authorization_header: # header 에서 'Authorization' 값이 없다면 출력
        return JsonResponse({"message": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)
    
    jwt_authenticator = JWTAuthentication() # JWTAuthentication 라이브러리를 토큰을 검증할 때 사용
    try: 
        validated_token = jwt_authenticator.get_validated_token(request.headers.get('Authorization').split(' ')[1]) # 토큰을 가져와 검증
        return str(validated_token) # 토근을 문자열로 반환
    
    except Exception as e: # 토큰 검증 후 유효하지 않을 때 출력
        return JsonResponse({"message": "Invalid token"}, status=status.HTTP_403_FORBIDDEN)

def get_user_info(token): # 검증된 토큰이 그대로 반환되었다면 토큰을 반환
    if isinstance(token, JsonResponse):
        return token 
    url = 'http://edm.japaneast.cloudapp.azure.com/api/user/info/' # 유저 정보를 조회할 때 사용하는 API 주소
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token, # 실제로 받는 토큰
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200: # API 응답에 성공 하였을 때
            data = response.json() # 응답받은 JSON 파일을 data에 저장
            user_info = data.get('user', {}) # data에서 유저 정보를 가져옴
            user_info['uuid'] = str(user_info.get('uuid', ''))  # uuid를 문자열로 변환
            return user_info

        else: # 토큰이 유효하지 않을 때 출력
            return JsonResponse({'error': f"Request failed with status code {response.status_code}"}, status=500)

    except Exception as e: # 오류 발생시 출력
        return JsonResponse({'error': f"An error occurred: {e}"}, status=500)

def get_user_meal(uuid, meal_time, meal_type): # 한끼 식사에 대한 정보 및 영양정보를 가져오는 함수
    user_uid_after = uuid.replace('-','') # DB에 저장된 uuid 형식은 '-'를 포함하지 않고 있기 때문에 '-' 문자를 제거
    user_meals = Usermeal.objects.filter(uuid=user_uid_after, meal_date=meal_time, meal_type = meal_type).values( # 식단 모델에서 uuid, meal_date, meal_type 가 모두 일치하는 모든 데이터를 받아옴
        'food_name',
        'imagelink', 
        'meal_serving', 
    # 외래키로 지정된 food_name 을 활용하여 food_name에 대한 영양정보들을 영양소 모델에서 데이터들을 모두 가져옴
        'food_name__carbs_g', 
        'food_name__protein_g', 
        'food_name__fat_g', 
        'food_name__sugar_g',
        'food_name__energy_kcal',
        'food_name__nat_mg',
        'food_name__col_mg',
    )
    
    meal_nutrient = []
    carbs, prot, fat, sugar, kcal, nat, col, mealserving = 0, 0, 0, 0, 0, 0, 0, 0
    imagelink = ""
    food_name, un_food_name = [], [] # 변수 초기화 및 선언


    for user_meal in user_meals: # 불러온 데이터들에서 하나의 식단 정보를 추출
        
        if user_meal['food_name__carbs_g'] != -1:   # -1은 영양소 정보가 없는 food_name에 모든 영양정보 값에 -1이 들어가 있음
                                                    # -1이 아닌 영양소 값이 들어 가 있다면 실행
            total = { # 식사에 대한 영양정보들을 meal_serving(식사량)에 맞춰서 저장 -> 식단 평가에 사용할 영양정보 추가
                'carbs': user_meal['food_name__carbs_g'] * user_meal['meal_serving'],
                'protein': user_meal['food_name__protein_g'] * user_meal['meal_serving'],
                'fat': user_meal['food_name__fat_g'] * user_meal['meal_serving'],
                'sugar': user_meal['food_name__sugar_g'] * user_meal['meal_serving'],
                'kcal' : user_meal['food_name__energy_kcal'] * user_meal['meal_serving'],
                'nat' : user_meal['food_name__nat_mg'] * user_meal['meal_serving'],
                'col' : user_meal['food_name__col_mg'] * user_meal['meal_serving'],
                'imagelink': user_meal['imagelink'],
                'food_name': user_meal['food_name'],
                'meal_serving': user_meal['meal_serving'],
                'un_food_name': "" # 음식 데이터가 없는 음식 이름을 저장하는 컬럼
                }
            meal_nutrient.append(total) # meal_nutrient 에 모든 데이터 추가
        
            imagelinks = [meal['imagelink'] for meal in meal_nutrient] # 한 끼 식사에 대한 이미지는 하나만 필요함
            if imagelinks: 
                imagelink = imagelinks[0] # 한 끼 식사에 대한 이미지는 첫 번째 값을 가져옴
            else:
                imagelink = "" # 이미지가 없으면 빈 문자열 반환

            food_name = [meal['food_name'] for meal in meal_nutrient] # 음식 이름을 리스트 형식으로 저장
            mealserving = [meal['meal_serving'] for meal in meal_nutrient] # 식사량을 리스트 형식으로 저장
            
            # meal_nutrient에 저장된 모든 영양 정보들의 합을 각 변수에 저장 
            carbs = sum_nutrients(meal_nutrient, 'carbs') 
            prot = sum_nutrients(meal_nutrient, 'protein')
            fat = sum_nutrients(meal_nutrient, 'fat')
            sugar = sum_nutrients(meal_nutrient, 'sugar')
            kcal = sum_nutrients(meal_nutrient, 'kcal')
            nat = sum_nutrients(meal_nutrient, 'nat')
            col = sum_nutrients(meal_nutrient, 'col')        

        
        else : # 영양정보에 -1 값이 들어가 있을 때
            total = { # 평가에 사용 될 모든 영양 정보를 0으로 저장 -> 영양정보에 없는 데이터의 음식은 영양정보를 합치지 않고 제외
                'carbs': 0,
                'protein': 0,
                'fat': 0,
                'sugar': 0,
                'kcal' : 0,
                'nat' : 0,
                'col' : 0,
                'imagelink': user_meal['imagelink'],
                'food_name': user_meal['food_name'],
                'meal_serving': user_meal['meal_serving'],
                'un_food_name': user_meal['food_name'],
                }
            meal_nutrient.append(total)
            
            imagelinks = [meal['imagelink'] for meal in meal_nutrient]
            if imagelinks:
                imagelink = imagelinks[0]
            else:
                imagelink = ""
                
            food_name = [meal['food_name'] for meal in meal_nutrient] 
            un_food_name= [meal['un_food_name'] for meal in meal_nutrient] # 영양소 모델에 없는 데이터의 이름을 un_food_name 칼럼에 저장
            

    return carbs, prot, fat, sugar, kcal, nat, col, imagelink, food_name, mealserving, un_food_name # 저장된 모든 영양소를 반환
        
    

def evaluate_date_meal(uuid, meal_date): # 하루에 대한 식사 정보 및 영양 정보를 반환하는 함수
    user_uid_after = uuid.replace('-','') 
    user_meals = Usermeal.objects.filter(uuid=user_uid_after, meal_date=meal_date).values( # 식단 모델에서 uuid 와 meal_date가 모두 일치하는 데이터들을 가져옴
        'meal_serving', 'food_name__carbs_g', 'food_name__protein_g', 'food_name__fat_g', 'food_name__sugar_g', 'food_name__energy_kcal', 'food_name__nat_mg', 'food_name__col_mg',
    )
    
    # 변수 선언 및 초기화
    meal_nutrient = []
    carbs, prot, fat, sugar, kcal, nat, col = 0, 0, 0, 0, 0, 0, 0
    
    for user_meal in user_meals:  
        
        if user_meal['food_name__carbs_g'] != -1:   # -1은 영양소 정보가 없는 food_name에 모든 영양정보 값에 -1이 들어가 있음
                                                    # -1이 아닌 영양소 값이 들어 가 있다면 실행
            
            total = { # 하루 식사의 영양 정보를 저장
                'carbs': user_meal['food_name__carbs_g'] * user_meal['meal_serving'],
                'protein': user_meal['food_name__protein_g'] * user_meal['meal_serving'],
                'fat': user_meal['food_name__fat_g'] * user_meal['meal_serving'],
                'sugar': user_meal['food_name__sugar_g'] * user_meal['meal_serving'],
                'kcal' : user_meal['food_name__energy_kcal'] * user_meal['meal_serving'],
                'nat' : user_meal['food_name__nat_mg'] * user_meal['meal_serving'],
                'col' : user_meal['food_name__col_mg'] * user_meal['meal_serving']
                }
            meal_nutrient.append(total) # meal_nutrient 에 모든 데이터 추가
            
            # meal_nutrient에 저장된 모든 영양 정보들의 합을 각 변수에 저장 
            carbs = sum_nutrients(meal_nutrient, 'carbs')
            prot = sum_nutrients(meal_nutrient, 'protein')
            fat = sum_nutrients(meal_nutrient, 'fat')
            sugar = sum_nutrients(meal_nutrient, 'sugar')
            kcal = sum_nutrients(meal_nutrient, 'kcal')
            nat = sum_nutrients(meal_nutrient, 'nat')
            col = sum_nutrients(meal_nutrient, 'col')
    
        else :
            total = { # 평가에 사용 될 모든 영양 정보를 0으로 저장 -> 영양정보에 없는 데이터의 음식은 평가에 적용되지 않기 위함
                'carbs': 0,
                'protein': 0,
                'fat': 0,
                'sugar': 0,
                'kcal' : 0,
                'nat' : 0,
                'col' : 0
                }
            meal_nutrient.append(total)

        
    return carbs, prot, fat, sugar, kcal, nat, col # 하루 식사에 대한 평가를 하기 위한 영양 정보를 반환 

def sum_nutrients(meal_nutrient, nutrient_key): # 영양소별로 더하는 함수
    return sum(item[nutrient_key] for item in meal_nutrient)

def evaluate_user_meal(token, meal_time): # 하루 식사를 평가하기 위해 데이터들을 가져오는 함수
    user_info = get_user_info(token)
    # token을 사용하여 유저 정보를 가져옴
    # 가져온 유저 정보에서 데이터 추출
    uuid = user_info.get('uuid', '')
    user_height = user_info.get('height', '')
    user_weight = user_info.get('weight', '')
    user_active_level = int(user_info.get('active_level', '')[0])
    user_birthdate = user_info.get('birthdate', '')
    user_diet_purpose = user_info.get('diet_purpose', '')
    user_gender = user_info.get('gender', '')
    
    # user_data 에 유저 데이터들을 모두 저장
    user_data = (user_height, user_weight, user_birthdate, user_gender, user_active_level, user_diet_purpose)
    # 사용자에 대한 알맞는 영양 정보들을 계산하는 calculate 함수에 user_data를 전달
    recommend_nutrients = calculate(*user_data)
    
    user_meal_nut = evaluate_date_meal(uuid, meal_time) # 하루의 식단에 대한 정보를 가져오는 함수
    diet_rating = evaluate(user_meal_nut, recommend_nutrients) # 가져온 식단 정보를 기반으로 평가하는 함수
    
    return diet_rating, user_meal_nut # 평가 정보와 하루의 식단 정보를 반환

def calculate_age(birth_date): # 현재 날짜를 기반으로 생일과 차이로 나이를 계산하는 함수
    today = datetime.now()
    birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def calculate_protein(weight, activity_level): 
    protein_factors = { # 운동량에 알맞는 단백질 계수 반환
        1: (0.8, 0.9),
        2: (1.0, 1.2),
        3: (1.2, 1.5),
        4: (1.5, 1.8),
        5: (2.0, 2.0)
    }

    min_factor, max_factor = protein_factors.get(activity_level, (0, 0))
    min_protein = weight * min_factor # 최소 단백질
    max_protein = weight * max_factor # 최대 단백질

    return min_protein, max_protein

def calculate(height, weight, birth_date, sex, activity_level, goal): # 사용자의 신체 정보를 기반하여 최적의 영양정보를 반환하는 함수 (독립적인 평가식 사용)
    age = calculate_age(birth_date)

    if sex == '남자': # 설계한 평가식을 바탕으로 계산된 '남자'에 대한 기준치
        base_rate = 66.47 + (13.75 * (weight-10) + (5 * height) - (6.76 * age))
    else: # 설계한 평가식을 바탕으로 계산된 '여자'에 대한 기준치  
        base_rate = 65.51 + (9.56 * (weight-10) + (1.85 * height) - (4.68 * age))

    activity_factors = {1: 0.1, 2: 0.2, 3: 0.375, 4: 0.5, 5: 0.725} # 활동량을 기준으로 평가식에 사용 될 계수 설정
    activity_rate = base_rate * activity_factors.get(activity_level, 0) # 활동량을 사용자 정보에서 받아옴

    goal_factors = {'체중 감량': -200, '체중 유지': 0, '체중증량': 200} # 계산식에 목표를 반영
    tdee = base_rate + activity_rate + goal_factors.get(goal, 0) # 목표를 사용자 정보에서 받아옴

    # tdee 는 일일 칼로리 카운터 값
    
    if sex == '남자' and tdee < 1500: 
        tdee = 1500
        goal_factors = {'체중 감량': -200, '체중 유지': 0, '체중증량': 200}
        tdee += goal_factors.get(goal, 0)
    elif sex == '여자' and tdee < 1000:
        tdee = 1000
        goal_factors = {'체중 감량': -200, '체중 유지': 0, '체중증량': 200}
        tdee += goal_factors.get(goal, 0)
    
    # 활동량에 따른 모든 영양소 계산 
    protein = calculate_protein(weight, activity_level) 
    fat = tdee * 0.2 / 9
    carbs = ((tdee - (protein[0] * 4 + fat * 9)) / 4, 
             (tdee - (protein[1] * 4 + fat * 9)) / 4)
    sugar = tdee * 0.1 / 4

    recommend = { # 사용자의 권장 영양정보 반환
        'age': int(age),
        'protein': protein,
        'fat': fat,
        'carbs': (carbs[0], carbs[1]),
        'sugar': sugar
    }

    return recommend

def evaluate(user_meal_nut, recommend): # 식단 평가 함수
    
    def calculate_error(recommend, actual): # 평가식을 사용한 사용자 권장 영양정보와 와 사용자가 등록한 식단의 영양정보의 오차를 반환하는 함수
        if isinstance(recommend, tuple):
            # 권장 범위를 기반으로 최소 및 최대 오차 계산
            min_error = abs((actual - recommend[0])) / recommend[0] * 100  
            max_error = abs((actual - recommend[1])) / recommend[1] * 100
            return min(min_error, max_error)
        else:
            return abs((actual - recommend)) / recommend * 100
    
    # 하루 식사에서 각 영양소들에 대한 오차를 반환
    carbs_error = calculate_error(recommend['carbs'], user_meal_nut[0])
    protein_error = calculate_error(recommend['protein'], user_meal_nut[1])
    fat_error = calculate_error(recommend['fat'], user_meal_nut[2])

    errors = [carbs_error, protein_error, fat_error]
    max_error = max(errors)

    # 오차를 비교하여 식단을 평가함
    if all(error <= 15 for error in errors):
        return 'Perfect'
    elif all(error <= 20 for error in errors):
        return 'Very Good'
    elif all(error <= 30 for error in errors):
        return 'Good'
    elif all(error <= 40 for error in errors):
        return 'Not Bad'
    elif max_error >= 50 or any(error > 40 for error in errors):
        return 'Bad'
    else:
        return 'Not Bad'

    
def save_user_evaluation(uuid, meal_date, diet_rating, user_meal_nut):
    # 이미 저장된 데이터가 있는지 확인
    existing_evaluation = Usermealevaluation.objects.filter(uuid=uuid, meal_date=meal_date)

    if existing_evaluation:
        # 이미 해당 조건을 만족하는 데이터가 있으면 삭제 후 생성 및 저장
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
  
