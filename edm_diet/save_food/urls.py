from django.urls import path
from . import views

urlpatterns = [
    path('api/save_new_food/', views.save_new_food_api, name='save_new_food_api'),
]
