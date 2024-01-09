from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/', views.subscribe,),
    path('subscribe/info/<str:uuid>/', views.get_user_name, name='get-user-name'),
    path('unsubscribe/<str:uuid>/', views.delete_subscription, name='delete-subscription'),
]