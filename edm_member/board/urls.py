from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# 라우터 생성
router = DefaultRouter()
router.register(r'asks', AskViewSet)


urlpatterns = [
    path('notices/', NoticeList.as_view(), name='notice-list'), # 공지 리스트 조회
    path('notices/<int:pk>/', NoticeDetailView.as_view(), name='notice-detail'), # 특정 공지 조회 
    path('faqs/', FAQList.as_view(), name='faq-list'), # FAQ 조회
    path('faqs/<int:pk>/', FAQDetailView.as_view(), name='faq-detail'), # 특정 FAQ 조회
    path('cardnews/', CardNewsListView.as_view(), name='cardnews-list'), # 카드뉴스 리스트 조회
    path('cardnews/<int:pk>/', CardNewsDetailView.as_view(), name='cardnews-detail'), # 특정 카드뉴스 조회
    path('', include(router.urls)), # 1대1 문의 CRUD
]