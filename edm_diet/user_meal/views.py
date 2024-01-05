from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Meal_Date.models import *
from Meal_Date.serializers import *
from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view,permission_classes
import requests
from datetime import datetime
from rest_framework.views import APIView
from rest_framework import generics
from datetime import datetime, timedelta
from collections import defaultdict

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

# 유저 식단 평가 조회
@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_meal_evaluation(request):
    token = validate_token(request)
    uuid = str(get_user_info(token).get('uuid',''))
    
    user_uid_after = uuid.replace('-','')

    user_meals_evaluation = list(Usermealevaluation.objects.filter(uuid=user_uid_after))
    
    meal_evaluation_serializers = UsermealevaluationSerializer(user_meals_evaluation,  many=True)
    
    user_meals_evaluation_data = [
    { 'meal_date': item['meal_date'], 'meal_evaluation': item['meal_evaluation'] } 
    for item in meal_evaluation_serializers.data
    ]
    response_data = {
    'user_meals_evaluation': user_meals_evaluation_data
    }
    
    return JsonResponse(response_data, safe=False)

class SaveUserMeal(APIView):
    serializer_class = MealSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message" : "User meal saved"
            })
        else:
            return Response({
                "message" : "User meal failed"
            })

# 유저 식단 저장
@api_view(['POST'])
def save_user_meal(request):
    
    token = validate_token(request)
    uuid = str(get_user_info(token).get('uuid',''))
    
    try:
        if request.data.get('inferResult') == '1':
        
        # 요청한 JSON 데이터 파싱
            data = request.data.get('predict', {}).get('ktFoodsInfo', {})
            meal_date = request.data.get('mealdate')
            meal_type = request.data.get('mealType')
            existing_evaluation = Usermeal.objects.filter(uuid=uuid, meal_date=meal_date, meal_type = meal_type)
            existing_evaluation.delete()
            for region_key, meal_data in data.items():
                Usermeal.objects.create( 
                    uuid = uuid,
                    meal_type = meal_type,
                    meal_date = meal_date,
                    imagelink = request.data.get('imagelink'),
                    food_name_id = meal_data.get('food_name')
                )
                
            return Response({"모두 저장 완료"}, status=status.HTTP_200_OK)
        
        else :
            
            data = request.data.get('predict', {}).get('foodNames', [])
            meal_date = request.data.get('mealdate')
            meal_type = request.data.get('mealType')
            existing_evaluation = Usermeal.objects.filter(uuid=uuid, meal_date=meal_date, meal_type = meal_type)
            existing_evaluation.delete()
                    
            for food_name in data:
                # Nutrient 모델에서 해당 food_name이 존재하는지 확인
                
                nutrient_obj = Nutrient.objects.filter(food_name=food_name).first()
                if nutrient_obj:
                    
                    print("save")
                    Usermeal.objects.create( 
                        uuid = uuid,
                        meal_type = meal_type,
                        meal_date = meal_date,
                        imagelink = request.data.get('imagelink'),
                        food_name = nutrient_obj,
                    )
                    
                else :
                    print("데이터베이스에 일치하는 데이터가 없습니다: ", food_name)
                
            return Response({"OCR 저장 완료"}, status=status.HTTP_200_OK)
        
                
    except Exception as e:
        # 데이터 처리 중 발생할 수 있는 예외 처리
        return Response({"message": f"오류: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def get_subscribe_meal_evaluation(request):
    uuid = request.query_params.get('uuid')
    user_uid_after = uuid.replace('-','')
    today = datetime.now()
    
    data_meal = list(Usermeal.objects.filter(uuid = user_uid_after,  meal_date__range=[today-timedelta(days=7),today]))
    data_evaluation = list(Usermealevaluation.objects.filter(uuid = user_uid_after, meal_date__range=[today-timedelta(days=7),today]))
    
    meal_serializers = MealSerializer(data_meal,  many=True)
    meal_evaluation_serializers = UsermealevaluationSerializer(data_evaluation,  many=True)
    
    # user_meals_data = [
    # {
    # 'meal_date': item['meal_date'],
    # 'meal_type': item['meal_type'],
    # 'imagelink' : item['imagelink'],
    # "predict":{
    #     "food_name": [item['food_name']], 
    #     }
    # }
    # for item in meal_serializers.data
    # ]
     
    user_meals_evaluation_data = [
    {
     'meal_date': item['meal_date'],
     'sum_carb': item['sum_carb'],
     'sum_sugar': item['sum_sugar'],
     'sum_protein': item['sum_carb'],
     'sum_fat': item['sum_fat'],
     'sum_col': item['sum_col'],
     'meal_evaluation': item['meal_evaluation'],
     } 
    for item in meal_evaluation_serializers.data
    ]
    
    unique_combinations = set()

    # 중복을 제거한 최종 결과물
    formatted_user_meals = []
    for meal_data in meal_serializers.data:
        meal_key = (meal_data['meal_date'], meal_data['meal_type'])
        if meal_key not in unique_combinations:
            unique_combinations.add(meal_key)
            formatted_user_meals.append({
                "mealType": meal_data["meal_type"],
                "mealdate": meal_data["meal_date"],
                "imagelink": meal_data["imagelink"],
                "predict": {
                    "foodNames": [meal_data["food_name"]],
                }
            })
        else:
        # 이미 존재하는 키에 대해 foodNames에 추가
            existing_meal = next(item for item in formatted_user_meals if item["mealdate"] == meal_data["meal_date"] and item["mealType"] == meal_data["meal_type"])
            existing_meal["predict"]["foodNames"].append(meal_data["food_name"])
            
# 최종 결과물을 user_meals_data에 반영
    user_meals_data = {"user_meals": formatted_user_meals}
    # unique_meals = defaultdict(list)

    # # user_meals 데이터 그룹화
    # for meal in user_meals_data["user_meals"]:
    #     key = (meal["meal_date"], meal["meal_type"], meal["imagelink"])
    #     unique_meals[key].append(meal["predict"]["food_name"][0])

    # # 최종 결과물 구성
    # user_meals_data = [
    #     {
    #         "mealType": meal["meal_type"],
    #         "mealdate": meal["meal_date"],
    #         "imagelink": meal["imagelink"],
    #         "predict": {
    #             "food_names": unique_meals[key],
    #         }
    #     }
    #     for key, food_names in unique_meals.items()
    # ]


    # # unique_user_meals_data = []
    # # unique_combinations = set()

    # # for meal_data in meal_serializers.data:
    # #     meal_key = (meal_data['meal_date'], meal_data['meal_type'], meal_data['imagelink'])
    # #     if meal_key not in unique_combinations:
    # #         unique_combinations.add(meal_key)
    # #         unique_user_meals_data.append(meal_data)
    
    response_data = {
    'user_meals_evaluation': user_meals_evaluation_data,
    'user_meals': user_meals_data,
    }
    
    return JsonResponse(response_data, safe=False)