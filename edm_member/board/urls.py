from django.urls import path
from .views import NoticeList, FAQList, NoticeDetailView, FAQDetailView

urlpatterns = [
    # 기존 URL 패턴들
    path('notices/', NoticeList.as_view(), name='notice-list'),
    path('notices/<int:pk>/', NoticeDetailView.as_view(), name='notice-detail'),
    path('faqs/', FAQList.as_view(), name='faq-list'),
    path('faqs/<int:pk>/', FAQDetailView.as_view(), name='faq-detail'),
]