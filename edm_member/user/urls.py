from django.urls import path, include
from . import views
from rest_framework import urls
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView


urlpatterns =[
    path('user/', views.CreateUser.as_view()),
    path('login/', views.Login.as_view(),),
    path("auth/refresh/",TokenRefreshView.as_view()), # access 토큰 재발급
    path('hello/', views.HelloWorldView.as_view(), name='hello_world'),
    # path('api-auth/', include('rest_framework.urls')),
]