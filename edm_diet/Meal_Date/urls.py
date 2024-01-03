from django.urls import include, path
from rest_framework import routers
from . import views

# router = routers.DefaultRouter()
# router.register(r'Meal', views.display_user_meal_evaluation, basename='meal')
# router.register(r'Nutrient', views.Nutrientviewset, basename='nutrient')

urlpatterns = [
    path('api/Meal/',views.display_user_meal_evaluation),
    # path('api/', include(router.urls)),
    # path('get_user_info/', views.get_user_info, name='get_user_info'),
    # path('evaluation/', views.Mealviewset.as_view({'get': 'list', 'post': 'create'}), name='test_evaluation'),
]
