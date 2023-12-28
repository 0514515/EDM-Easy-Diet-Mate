from django.urls import path, include
from . import views
from rest_framework import urls
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns =[
    path('user/', views.CreateUser.as_view()), # 유저 생성
    path('login/', views.Login.as_view(),), # 로그인
    path('auth/refresh/',TokenRefreshView.as_view()), # access 토큰 재발급
    path('user/info/',views.user_info), # 유저 정보 조회, 수정, 삭제
    
    
    # path('api-auth/', include('rest_framework.urls')),
]