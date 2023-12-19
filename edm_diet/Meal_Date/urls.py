from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter() # DefaultRouter 설정
router.register('Meal', views.MealViewSet, basename = 'meal') # Mealviewset과 Meal_Date 이라는 router 등록

urlpatterns = [
    path('add/', views.MealViewSet.as_view()),
    path('calender/', include(router.urls)),
]