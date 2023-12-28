from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'Meal', views.Mealviewset, basename='meal')
router.register(r'Nutrient', views.Nutrientviewset, basename='nutrient')

urlpatterns = [
    path('api/', include(router.urls)),
    path('evaluation/', views.Mealviewset.as_view({'get': 'list', 'post': 'create'}), name='test_evaluation'),
    path('user_meal_evaluation/', views.display_user_meal_evaluation, name='user_meal_evaluation'),
]
