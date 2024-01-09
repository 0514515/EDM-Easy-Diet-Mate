from django.urls import include, path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('get_meal/', views.get_user_meal_evaluation, name='get_meal'),
    path('save_user_meal/', views.save_user_meal, name='save_meal'),
    path('subscribe/',views.get_subscribe_meal_evaluation, name='subscribe'),
    path('upload/', views.ImageView.as_view(), name='image_upload'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)