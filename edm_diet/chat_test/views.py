from django.shortcuts import render
import openai
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.conf import settings
from datetime import datetime,timedelta
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from Meal_Date.models import *
from Meal_Date.views import *
 
# model, key 받아오는 부분
class OpenAI_Client:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key
 
    def chat_completion(self, model, messages, max_tokens):
        return openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens
        )
       
# 사용자 채팅 - 일상생활 대화:0, 식단평가 문의:1로 분류
binary_model = 'ft:gpt-3.5-turbo-1106:personal::8dZMIYUW'
 
# chatAPI key - settings.py 에 숨겨둠
API_KEY1 = settings.API_KEY1
 
 
# token
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
 
@csrf_exempt
@api_view(['POST'])
# Django 뷰 함수    
def chatbot_view(request):
    if request.method == 'POST':
        try:
            token = validate_token(request)
            uuid = str(get_user_info(token).get('uuid',''))
           
            # 1. font에서 입력한 사용자 message
            data = json.loads(request.body.decode('utf-8'))
            inputText = data.get('message')
           
            if not inputText:
                return HttpResponseBadRequest("No message provided")
           
            # 2. OpenAI API를 이용한 처리
            # OpenAI key
            key1 = OpenAI_Client(API_KEY1)
            # chatGPT 함수에서 나온 결과(ai 답변) 저장
            response = chatGPT(inputText, key1, uuid)
            # response 출력
            print(response)
           
            # 3. front에 답변 전달
            return JsonResponse({'message': response})
 
        except json.JSONDecodeError:
            return JsonResponse({'error':'Invalid JSON'}, status=400)
 
    else:
        return JsonResponse({'error' : 'Method not allowed'}, status=405)
       
# 대화 이진 분류 -> 결과 반환 함수
def chatGPT(inputText, key1, uuid):
    # 1. 일상 생활(0) / 식단 평가 대화(1) 분류
    response = key1.chat_completion(
        model= binary_model,
        messages=[
            {"role": "system", "content": "너는 식단을 평가해주는 챗봇이야"},
            {"role": "user", "content": inputText},
        ],
        max_tokens=150,
    )
   
    # 0또는 1로 분류된 결과
    result = response["choices"][0]["message"]["content"]
   
    # 사용자의 기록된 식단 DB
    today = datetime.now()  # 날짜별 기록 결과 확인 위함
    user_uid_after = uuid.replace('-','')
   
    # 기록 날짜, 탄수화물, 당, 단백질, 지방, 식단평가결과, 총 칼로리 데이터 참조
    user_meals = Usermealevaluation.objects.filter(uuid=user_uid_after, meal_date__range=[today-timedelta(days=7),today]).values(
            'meal_date', 'sum_carb', 'sum_sugar', 'sum_protein', 'sum_fat', 'meal_evaluation', 'sum_kcal'
            )  
     
    # 2. 식단 평가 대화 : 1
    if result == "assistant: 1":
        diet_response = key1.chat_completion(
        model = 'gpt-4',
        messages = [
            {"role": "system", "content": "너는 max_tokens가 있어도 문장을 뚝 끊지 않고 자연스럽게 마무리해주는 식단 평가 결과 분석 챗봇이야."},
            {"role": "user", "content": inputText},
            # 사용자의 채팅에서 날짜 추출 assistant
            {"role":"assistant",
            "content": f"""
            너는 식단 평가 결과를 궁금해 하는 사용자와 대화하는 친절한 결과 분석 챗봇이야. 사용자의 데이터는 {user_meals} 이걸 참고해줘. 날짜, 탄수화물, 당, 단백질, 지방, 식단 평가 결과, 총칼로리가 포함되어 있다.
            오늘은 {today.strftime('%Y-%m-%d')}이다.  사용자 입력 문장에서 (어제, 하루 전, 1일전, 하루전, 이틀 전, 이틀전, 2일전, 2일 전, 그저께, 엊그제, 엊그저께, 3일전, 3일 전, 일주일전, 일주일 전, 저번 주) 등을 포착해서 사용자가 요구하는 날짜가 출력하고 해당 날짜의 식단 평가 결과를 분석해줘.
            문장 속에서 날짜를 찾을 수 없다면 '구체적인 날짜를 입력해주세요' 출력하고, 특정 날짜의 정보가 존재하지 않으면 ''특정 날짜'의 식단 정보가 존재하지 않습니다'라고 출력해줘.
            """},
        ],
        # 최대 토큰 수 제한
        max_tokens = 300,
        )
        # 식단 평가 분석 질문에 대한 답변
        diet_result = diet_response["choices"][0]["message"]["content"]
        # diet_result 반환
        return diet_result
   
    # 3. 일상 생활 대화 : 0
    else:
        daily_response = key1.chat_completion(
        model = 'gpt-4',
        messages = [
            {"role": "system", "content": "너는 max_tokens가 있어도 문장을 뚝 끊지 않고 마무리해줘."},
            {"role": "user", "content": inputText},
        ],
        # 최대 토큰 수 제한
        max_tokens = 300,
        )
        # 일상 대화에 대한 답변
        daily_result = daily_response["choices"][0]["message"]["content"]
        # daily_result 반환
        return daily_result