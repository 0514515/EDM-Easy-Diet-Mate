from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/', views.subscribe,), # 구독 리스트 조회, 구독 추가
    path('subscribe/info/<str:uuid>/', views.get_user_name, name='get-user-name'), # 구독 1명 이름 조회
    path('unsubscribe/<str:uuid>/', views.delete_subscription, name='delete-subscription'), # 구독 1개 삭제
]