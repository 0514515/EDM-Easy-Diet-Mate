import pdb
import requests

url = "http://127.0.0.1:8000/Meal_Date/test2/Meal/?format=api"

response = requests.get(url)

pdb.set_trace()

if response.status_code == 200:
    data = response.json()
    print("응답 데이터:", data)
else:
    print("요청 실패. 상태 코드:", response.status_code)
    # evaluate_user_meal 함수 호출
