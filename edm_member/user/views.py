
from .serializers import *
from .models import User
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view

def user_response(message="", display_message="",status=status.HTTP_400_BAD_REQUEST):
    return Response(
        {
            "message": message,
            "display_message": display_message
        },
        status=status
    )

# 회원가입
class CreateUser(generics.CreateAPIView):
    # permission_classes = [IPBasedPermission]
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer
    
    def post(self, request, *args, **kwargs):
        
        user = User.objects.filter(email=request.data['email'])
        
        # 회원 존재 여부 확인
        if user:
            return user_response(
                message="user is already exists",
                display_message="이미 존재하는 회원입니다.",
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return self.create(request, *args, **kwargs)

class Login(APIView):
    serializer_class = LoginUserSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email=email).first()
        
        print(UserInfoSerializer(user).data)

        try:
            # 계정 없을 때
            if not user:
                print("user is not exists")
                return user_response(
                    message="user is not exists",
                    display_message="존재하지 않는 회원입니다.",
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # 비밀번호 틀렸을 때
            if not check_password(password, user.password):
                print("password is not valid")
                return user_response(
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
                        "user" : UserInfoSerializer(user).data,
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                    status=status.HTTP_200_OK
                )
                
                # response.set_cookie("access_token",access_token,httponly=True)
                # response.set_cookie("refresh_token",refresh_token,httponly=True)
                return response
            
            else:
                return user_response(
                    message="login failed",
                    display_message="로그인에 실패하였습니다",
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return user_response(
                message="unknown error",
                display_message="로그인에 실패했습니다.",
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['GET','PATCH','DELETE'])
def delete_or_patch(request):
    if request.method=='PATCH':
        try:
            data = UpdateUserSerializer(request.data).data
            
            user = User.objects.filter(uuid=data["uuid"]).first()
            
            if not user:
                print("user is not exists")
                return user_response(
                    message="user is not exists",
                    display_message="존재하지 않는 회원입니다.",
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            serializer = UpdateUserSerializer(user, data=data, partial=True)
            print(serializer)
            
            if serializer.is_valid():
                serializer.save()
                return user_response(
                    display_message="회원 수정이 완료되었습니다.",
                    message="update user success",
                    status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return user_response(
                display_message="회원 수정에 실패하였습니다.",
                message="patch user failed",
                status=status.HTTP_400_BAD_REQUEST
            )
    
    
    elif request.method=='DELETE':
        
        try:
            email = request.data['email']
            password = request.data['password']
            uuid = request.data['uuid']
            
            user1 = User.objects.filter(uuid=uuid).first()
            user2 = User.objects.filter(email=email).first()
            
            if not user1:
                print("user is not exists")
                return user_response(
                    message="user is not exists",
                    display_message="존재하지 않는 회원입니다.",
                    status=status.HTTP_400_BAD_REQUEST
                )
                    
            if user1 != user2:
                print("invalid email")
                return user_response(
                    message="invalid email",
                    display_message="이메일이 틀렸습니다.",
                    status=status.HTTP_400_BAD_REQUEST
                )
                    
            # 비밀번호 틀렸을 때
            if not check_password(password, user1.password):
                print("password is not valid")
                return user_response(
                    message="password is not valid",
                    display_message="비밀번호가 틀렸습니다.",
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            if (email==user1.email) and check_password(password, user1.password):
                # 삭제
                user1.delete()
                return user_response(
                    display_message="회원탈퇴에 성공하였습니다.",
                    message="delete user success",
                    status=status.HTTP_200_OK
                )
                
            return user_response(
                display_message="회원 삭제에 실패하였습니다.",
                message="delete user failed",
                status=status.HTTP_400_BAD_REQUEST
            )
        except:
            return user_response(
                display_message="회원 삭제에 실패하였습니다.",
                message="delete user failed",
                status=status.HTTP_400_BAD_REQUEST
            )
          
    elif request.method=='GET':
        try:
            data = UpdateUserSerializer(request.data).data
            
            user = User.objects.filter(uuid=data["uuid"]).first()
            
            if not user:
                print("user is not exists")
                return user_response(
                    message="user is not exists",
                    display_message="존재하지 않는 회원입니다.",
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            serializer = UpdateUserSerializer(user, data=data, partial=True)
            print(serializer)
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "user" : UserInfoSerializer(user).data,
                }
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return user_response(
                display_message="회원 조회에 실패하였습니다.",
                message="patch user failed",
                status=status.HTTP_400_BAD_REQUEST
            )
        
    else:
        return Response({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# class UserInfoApi(APIView):
# uuid 기반 유저 정보 단일 조회
# class GetUserInfo(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserInfoSerializer
#     lookup_field = 'uuid'
    

# class UpdateUserInfo(generics.UpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UpdateUserSerializer
#     lookup_field = 'uuid'


# class DeleteUserInfo(generics.DestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = DeleteUserSerializer
#     lookup_field = 'uuid'

            
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
