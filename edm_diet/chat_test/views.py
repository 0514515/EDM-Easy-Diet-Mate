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
        
        
#binary_model = 'ft:gpt-3.5-turbo-0613:personal::8aQw2MU1'
binary_model = 'ft:gpt-3.5-turbo-1106:personal::8dZMIYUW'

# settings에 들어감
API_KEY1 = settings.API_KEY1
API_KEY2 = settings.API_KEY2

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
            
            data = json.loads(request.body.decode('utf-8'))
            print(data)
            inputText = data.get('message')
            # inputText = "12월 17일 식단 어땠지?"
            print(inputText)
            
            if not inputText:
                return HttpResponseBadRequest("No message provided")

            key1 = OpenAI_Client(API_KEY1)
            key2 = OpenAI_Client(API_KEY2)
            
            # OpenAI API를 이용한 처리
            response = chatGPT(inputText, key1, key2, uuid)
            print(response)
            return JsonResponse({'message': response})

        except json.JSONDecodeError:
            return JsonResponse({'error':'Invalid JSON'}, status=400)

    else:
        return JsonResponse({'error' : 'Method not allowed'}, status=405)
        

def chatGPT(inputText, key1, key2, uuid):
    
    response = key2.chat_completion(
        model= binary_model,
        messages=[
            {"role": "system", "content": "너는 식단을 평가해주는 챗봇이야"},
            {"role": "user", "content": inputText},
        ],
        max_tokens=150,
    )
    
    result = response["choices"][0]["message"]["content"]
    print(result)
    today = datetime.now()
    
    # DB
    user_uid_after = uuid.replace('-','')
    user_meals = Usermealevaluation.objects.filter(uuid=user_uid_after, meal_date__range=[today-timedelta(days=7),today]).values(
            'meal_date', 'sum_carb', 'sum_sugar', 'sum_protein', 'sum_fat', 'meal_evaluation', 'sum_kcal'
            )   
      
    # 식단 평가 대화 : 1
    if result == "assistant: 1":
        diet_response = key2.chat_completion(
        model = 'gpt-4',
        messages = [
            {"role": "system", "content": "너는 max_tokens가 있어도 문장을 뚝 끊지 않고 마무리해주는 식단 평가 결과 분석 챗봇이야."},
            {"role": "user", "content": inputText},
            {"role":"assistant", 
            "content": f"너는 식단 평가 결과를 궁금해 하는 사용자와 대화하는 친절한 결과 분석 챗봇이야. 사용자의 DB가 너한테 투입될 예정이야. 일단  {user_meals} 이거 참고해줘. 오늘은 {today.strftime('%Y-%m-%d')}이다.  사용자 입력 문장에서 (어제, 하루 전, 1일전, 하루전, 이틀 전, 이틀전, 2일전, 2일 전, 그저께, 엊그제, 엊그저께, 3일전, 3일 전, 일주일전, 일주일 전, 저번 주) 등을 포착해서 사용자가 요구하는 날짜가 언제인지 출력해줘. 사용자의 다른 요구사항은 무시하고, 문장 속에서 찾을 수 있는 날짜만 'yyyy-mm-dd' 형식으로 출력해줘. 문장 속에서 날짜를 찾을 수 없다면 '구체적인 날짜를 입력해주세요' 출력하고, 특정 날짜의 정보가 존재하지 않으면 ''특정 날짜'의 식단 정보가 존재하지 않습니다'라고 출력해줘."},
        ],
        max_tokens = 300,
        )
        diet_result = diet_response["choices"][0]["message"]["content"]
        # diet_result를 front에 전달
        print("식단평가 bot")
        return diet_result
    
    # 일상 생활 대화 : 0
    else:
        daily_response = key2.chat_completion(
        model = 'gpt-4',
        messages = [
            {"role": "system", "content": "너는 max_tokens가 있어도 문장을 뚝 끊지 않고 마무리해주는 챗봇이야."},
            {"role": "user", "content": inputText},
        ],
        max_tokens = 150,
        )
        daily_result = daily_response["choices"][0]["message"]["content"]
        print("일상대화 bot")
        return daily_result

