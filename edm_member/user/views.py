
from .serializers import *
from .models import User
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

def user_error_response(message="", display_message="",status=status.HTTP_400_BAD_REQUEST):
    return Response(
        {
            "message": message,
            "display_message": display_message
        },
        status=status
    )

# 회원가입
class CreateUser(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer
    
    def post(self, request, *args, **kwargs):
        
        user = User.objects.filter(email=request.data['email'])
        
        # 회원 존재 여부 확인
        if user:
            return user_error_response(
                message="user is already exists",
                display_message="이미 존재하는 회원입니다.",
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return self.create(request, *args, **kwargs)

class Login(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email=email).first()

        # 계정 없을 때
        if not user:
            return user_error_response(
                message="user is not exists",
                display_message="존재하지 않는 회원입니다.",
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # 비밀번호 틀렸을 때
        if not check_password(password, user.password):
            return user_error_response(
                message="password is not valid",
                display_message="비밀번호가 틀렸습니다.",
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # 정보 다 맞으면
        if user is not None:
  
            token = TokenObtainPairSerializer.get_token(user) # 리프레시 토큰 생성
            refresh_token = str(token)
            access_token = str(token.access_token)
            
            response = Response(
                {
                    "access": access_token,
                    "refresh": refresh_token,
                },
                status=status.HTTP_200_OK
            )
            
            # response.set_cookie("access_token",access_token,httponly=True)
            # response.set_cookie("refresh_token",refresh_token,httponly=True)
            return response
        
        else:
            return Response(
                {"message","로그인에 실패하였습니다"}, status=status.HTTP_400_BAD_REQUEST
            )
            
# class DeleteUser(APIView):
#     def post(self, request):
#         email = request.data['email']
#         password = request.data['password']
        
#         user = User.objects.filter(email=email).first()

#         # 계정 없을 때
#         if is_user_exist(email):
#             return user_error_response(
#                 message="user is not exists",
#                 display_message="존재하지 않는 회원입니다.",
#                 status=status.HTTP_400_BAD_REQUEST
#             )
            
#         # 비밀번호 틀렸을 때
#         if not check_password(password, user.password):
#             return user_error_response(
#                 message="password is not valid",
#                 display_message="비밀번호가 틀렸습니다.",
#                 status=status.HTTP_400_BAD_REQUEST
#             )
            
#         # 정보 다 맞으면
#         if user is not None:
  
#             token = TokenObtainPairSerializer.get_token(user) # 리프레시 토큰 생성
#             refresh_token = str(token)
#             access_token = str(token.access_token)
            
#             response = Response(
#                 {
#                     "access": access_token,
#                     "refresh": refresh_token,
#                 },
#                 status=status.HTTP_200_OK
#             )
            
#             # response.set_cookie("access_token",access_token,httponly=True)
#             # response.set_cookie("refresh_token",refresh_token,httponly=True)
#             return response
        
#         else:
#             return Response(
#                 {"message","로그인에 실패하였습니다"}, status=status.HTTP_400_BAD_REQUEST
#             )

# # 회원탈퇴
# class DeleteUser(generics.DestroyAPIView):
#     queryset
