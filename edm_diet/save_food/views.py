from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Meal_Date.models import *

@api_view(['POST'])
def save_new_food_api(request):

    try:
        # 요청한 JSON 데이터 파싱
        data = request.data.get('predict', {}).get('ktFoodsInfo', {})

        # 기존 데이터와 일치하지 않는 항목을 저장할 리스트
        non_matching_data = []
        
        for region_key, food_data in data.items(): 
            food_object, created = Nutrient.objects.get_or_create( # 영양정보 모델에 데이터가 없으면 데이터를 받아와서 저장
                food_name=food_data.get('food_name'),
                defaults={
                    "food_name" : food_data.get('food_name'),
                    "weight_g" : food_data.get('food_serving_size'),
                    "energy_kcal" : food_data.get('food_cal'),
                    "carbs_g" : food_data.get('food_carbs'),
                    "sugar_g" : food_data.get('food_sugar'),
                    "fat_g" : food_data.get('food_fat'),
                    "protein_g" : food_data.get('food_protein'),
                    "nat_mg" : food_data.get('food_nat'),
                    "col_mg" : food_data.get('food_cholesterol'),
                }
            )
            
            if created:
                non_matching_data.append({"message": f"데이터가 성공적으로 저장되었습니다 - {food_data.get('food_name')}", "data": food_object.serialize()})
            else:
                non_matching_data.append({"message": f"데이터가 이미 존재합니다 - {food_data.get('food_name')}", "data": food_object.serialize()})

        return Response({"non_matching_data": non_matching_data}, status=status.HTTP_200_OK) # 영양정보 모델에 없는 데이터들을 반환

    except Exception as e:
        
        # 데이터 처리 중 발생할 수 있는 예외 처리
        return Response({"non_matching_data": non_matching_data}, status=status.HTTP_200_OK)