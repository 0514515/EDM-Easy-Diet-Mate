from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('api/Meal/',views.display_user_meal_evaluation), 
]
