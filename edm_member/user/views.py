from django.shortcuts import render
from .serializers import UserSerializer
from .models import User
from rest_framework import generics

# 회원가입
class CreateUser(generics.CreateAPIView):
    queryset = User.manager.all()
    serializer_class = UserSerializer
