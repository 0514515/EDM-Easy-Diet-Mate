from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# 라우터 생성
router = DefaultRouter()
router.register(r'asks', AskViewSet)


urlpatterns = [
    path('notices/', NoticeList.as_view(), name='notice-list'),
    path('notices/<int:pk>/', NoticeDetailView.as_view(), name='notice-detail'),
    path('faqs/', FAQList.as_view(), name='faq-list'),
    path('faqs/<int:pk>/', FAQDetailView.as_view(), name='faq-detail'),
    path('cardnews/', CardNewsListView.as_view(), name='cardnews-list'),
    path('cardnews/<int:pk>/', CardNewsDetailView.as_view(), name='cardnews-detail'),
    path('', include(router.urls)),
]