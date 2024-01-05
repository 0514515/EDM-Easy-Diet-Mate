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

    user_meals = list(Usermeal.objects.filter(uuid=user_uid_after))
    user_meals_evaluation = list(Usermealevaluation.objects.filter(uuid=user_uid_after))
    
    meal_serializers = MealSerializer(user_meals,  many=True)
    meal_evaluation_serializers = UsermealevaluationSerializer(user_meals_evaluation,  many=True)

    user_meals_data = meal_serializers.data
    #user_meals_evaluation_data = meal_evaluation_serializers.data
    
    user_meals_evaluation_data = [
    { 'meal_date': item['meal_date'], 'meal_evaluation': item['meal_evaluation'] } 
    for item in meal_evaluation_serializers.data
    ]
    response_data = {
    'user_meals_evaluation': user_meals_evaluation_data
    }
    # response_data = {
    #     'user_meals_data': user_meals_data, 
    #     'user_meals_evaluation': user_meals_evaluation_data
    # }
    
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
            for region_key, meal_data in data.items():
                Usermeal.objects.create( 
                    uuid = uuid,
                    meal_type = request.data.get('mealType'),
                    meal_date = request.data.get('mealdate'),
                    imagelink = request.data.get('imagelink'),
                    food_name_id = meal_data.get('food_name'),
                )
                
            return Response({"모두 저장 완료"}, status=status.HTTP_200_OK)
        
        else :
            
            data = request.data.get('predict', {}).get('foodNames', [])
            meal = MealSerializer(data=request.data)
            print(meal)
            for food_name in data:
                # Nutrient 모델에서 해당 food_name이 존재하는지 확인
                nutrient_obj = Nutrient.objects.filter(food_name=food_name).first()
                if nutrient_obj:
                    Usermeal.objects.create(
                        uuid=uuid,
                        meal_type = request.data.get('mealType'),
                        meal_date = request.data.get('mealdate'),
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
