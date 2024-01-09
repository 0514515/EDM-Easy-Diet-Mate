# Create your views here.
from rest_framework import generics
from .models import FAQ, Notice, CardNews
from rest_framework.permissions import AllowAny
from .serializers import *
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

# FAQ 리스트 조회
class FAQList(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

# 공지 리스트 조회
class NoticeList(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    

# 공지 상세 조회
class NoticeDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

# FAQ 상세 조회
class FAQDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

# 카드뉴스 리스트 조회
class CardNewsListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = CardNews.objects.all()
    serializer_class = CardNewsSerializer

# 카드뉴스 1건 조회
class CardNewsDetailView(generics.RetrieveAPIView):
    queryset = CardNews.objects.all()
    serializer_class = CardNewsSerializer
    
# 1대1 문의 Viewset
class AskViewSet(viewsets.ModelViewSet):
    queryset = Ask.objects.all()
    serializer_class = AskSerializer

    def get_queryset(self):
        # 유저의 UUID를 기반으로 쿼리셋 필터링
        user_uuid = self.request.user.uuid
        return Ask.objects.filter(user__uuid=user_uuid)

    def perform_create(self, serializer):
        # 생성 시, 자동으로 현재 유저 할당
        serializer.save(user=self.request.user)
        
    def destroy(self, request, *args, **pk):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "삭제가 완료되었습니다."}, status=status.HTTP_200_OK)