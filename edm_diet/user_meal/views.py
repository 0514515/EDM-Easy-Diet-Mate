from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Meal_Date.models import *
from Meal_Date.serializers import *
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view,permission_classes
import requests
from datetime import datetime
from rest_framework.views import APIView
from datetime import datetime, timedelta
from operator import itemgetter


def validate_token(request):
    authorization_header = request.headers.get('Authorization') # header 에서 'Authorization'에서 사용자의 토큰을 받아옴
    if not authorization_header: # header 에서 'Authorization' 값이 없다면 출력
        return JsonResponse({"message": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)
    
    jwt_authenticator = JWTAuthentication() # JWTAuthentication 라이브러리를 사용하여 토큰을 검증
    try:
        validated_token = jwt_authenticator.get_validated_token(request.headers.get('Authorization').split(' ')[1])
        return str(validated_token)
    
    except Exception as e:
        return JsonResponse({"message": "Invalid token"}, status=status.HTTP_403_FORBIDDEN)

def get_user_info(token):
    if isinstance(token, JsonResponse): # 토큰이 그대로 반환되었다면 
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

        else:
            return JsonResponse({'error': f"Request failed with status code {response.status_code}"}, status=500)

    except Exception as e:
        return JsonResponse({'error': f"An error occurred: {e}"}, status=500)


class ImageView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = ImagesaveSerializer(data=request.data)

        if file_serializer.is_valid():
            imagesave_instance = file_serializer.save()
            image_url = request.build_absolute_uri(imagesave_instance.imagelink.url)
            return Response({'imagelink': image_url}, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    { 'meal_date': item['meal_date'], 'meal_evaluation': item['meal_evaluation'], 'sum_carb' : item['sum_carb'], 'sum_protein' : item['sum_protein']} 
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
            
        data = request.data.get('predict', {}).get('foodNames', [])
        meal_date = request.data.get('mealdate')
        meal_type = request.data.get('mealType')
        
        servings = request.data.get('predict', {}).get('serving', [])
        
        existing_evaluation = Usermeal.objects.filter(uuid=uuid, meal_date=meal_date, meal_type = meal_type)
        existing_evaluation.delete()
               
        non_food_data = []
        print(data, "data 출력")        
        for food_name in data:
            # Nutrient 모델에서 해당 food_name이 존재하는지 확인
            
            nutrient_obj = Nutrient.objects.filter(food_name=food_name).first()
            
            if nutrient_obj :
                
                meal_serving = float(servings.pop(0)) if servings else 1.0
                Usermeal.objects.create( 
                    uuid = uuid,
                    meal_type = meal_type,
                    meal_date = meal_date,
                    imagelink = request.data.get('imagelink'),
                    food_name = nutrient_obj,
                    meal_serving = meal_serving,
                )
                
            else :
                
                new_data = Nutrient.objects.create(  
                        food_name = food_name,
                        weight_g = -1,
                        energy_kcal = -1,
                        carbs_g = -1,
                        sugar_g = -1,
                        fat_g = -1,
                        protein_g = -1,
                        nat_mg = -1,
                        col_mg = -1,
                )
                non_food_data.append(food_name)
                
                meal_serving = float(servings.pop(0)) if servings else 1.0
                Usermeal.objects.create( 
                        uuid = uuid,
                        meal_type = meal_type,
                        meal_date = meal_date,
                        imagelink = request.data.get('imagelink'),
                        food_name = new_data,
                        meal_serving = meal_serving,
                    )
                      
        return Response({"식단 저장 완료"}, status=status.HTTP_200_OK)
        
                
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

     
    user_meals_evaluation_data = [
    {
     'meal_date': item['meal_date'],
     'sum_carb': item['sum_carb'],
     'sum_sugar': item['sum_sugar'],
     'sum_protein': item['sum_protein'],
     'sum_fat': item['sum_fat'],
     'sum_col': item['sum_col'],
     'sum_nat': item['sum_nat'],
     'meal_evaluation': item['meal_evaluation'],
     } 
    for item in meal_evaluation_serializers.data
    ]
    
    user_meals_evaluation_data = sorted(user_meals_evaluation_data, key=itemgetter('meal_date'))
    
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
            existing_meal = next(item for item in formatted_user_meals if item["mealdate"] == meal_data["meal_date"])
            existing_meal["predict"]["foodNames"].append(meal_data["food_name"])
            
# 최종 결과물을 user_meals_data에 반영
    user_meals_data = {"user_meals": formatted_user_meals}
    
    response_data = {
    'user_meals_evaluation': user_meals_evaluation_data,
    'user_meals': user_meals_data,
    }
    
    return JsonResponse(response_data, safe=False)