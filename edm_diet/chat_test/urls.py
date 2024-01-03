from django.urls import include, path
from django.contrib import admin
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('chatAPI/', views.chatbot_view, name='chatAPI'),
]
 