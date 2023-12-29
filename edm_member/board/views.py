# Create your views here.
from rest_framework import generics
from .models import FAQ, Notice, CardNews
from rest_framework.permissions import AllowAny
from .serializers import FAQSerializer, NoticeSerializer,CardNewsSerializer

class FAQList(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

class NoticeList(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    
    
class NoticeDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

class FAQDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    
class CardNewsListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = CardNews.objects.all()
    serializer_class = CardNewsSerializer

class CardNewsDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = CardNews.objects.all()
    serializer_class = CardNewsSerializer