
from .serializers import *
from .models import *
from subscribe.models import *
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
import re
from .serializers import PasswordResetSerializer
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


def user_response(message="", display_message="",status=status.HTTP_400_BAD_REQUEST):
    return Response(
        {
            "message": message,
            "display_message": display_message
        },
        status=status
    )
    
@api_view(['POST'])
@permission_classes([AllowAny])
def check_email_existence(request):
    email = request.data.get('email', '')

    if not email:
        return Response(
            {'message': '이메일은 필수입니다.', 'display_message': '이메일 주소를 입력하세요.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not re.match(r'^[\w\.-]+@[\w\.-]+$', email):
        return Response(
            {'message': '유효한 이메일 형식이 아닙니다.', 'display_message': '유효한 이메일 주소를 입력하세요.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 이메일이 이미 존재하는지 확인합니다.
    if User.objects.filter(email=email).exists():
        return Response(
            {'message': '이미 사용 중인 이메일입니다.', 'display_message': '이미 사용 중인 이메일입니다.'},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {'message': '사용 가능한 이메일입니다.', 'display_message': '사용 가능한 이메일입니다.'},
            status=status.HTTP_200_OK
        )

# 회원가입
class CreateUser(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # 개인정보 처리방침에 동의했는지 확인
            if not serializer.validated_data.get('agreed_to_privacy_policy', False):
                return Response({
                    'message' : 'agreement must be True',
                    'display_message': "개인정보 처리방침에 동의해야 합니다."
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                return self.create(request, *args, **kwargs)
            except UserAlreadyExistsException as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # 유효성 검증에 실패한 경우의 에러 메시지
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

@api_view(['GET','PATCH','POST'])
@permission_classes([IsAuthenticated])
def user_info(request):
    
    jwt_authenticator = JWTAuthentication()
    try:
        validated_token = jwt_authenticator.get_validated_token(request.headers.get('Authorization').split(' ')[1])
        uuid = jwt_authenticator.get_user(validated_token).uuid

    except Exception as e:
        return Response({"message": "Invalid token"}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method=='PATCH':
        try:
            user = User.objects.filter(uuid=uuid).first()
            data = request.data
            if data['height']=='':
                data['height']=user.height
            if data['weight']=='':
                data['weight']=user.weight
            data = UpdateUserSerializer(request.data).data
            
            
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
                print(data['height'])
                serializer.update(instance=user,validated_data=data)
                return user_response(
                    display_message="회원 수정이 완료되었습니다.",
                    message="update user success",
                    status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return user_response(
                display_message="회원 수정에 실패하였습니다.",
                message="patch user failed",
                status=status.HTTP_400_BAD_REQUEST
            )
    
    
    elif request.method=='POST':
        
        try:
            email = request.data['email']
            password = request.data['password']
            
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
            
            user = User.objects.filter(uuid=uuid).first()
            
            if not user:
                print("user is not exists")
                return user_response(
                    message="user is not exists",
                    display_message="존재하지 않는 회원입니다.",
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            serializer = UpdateUserSerializer(user, data=data, partial=True)
            
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
                message="search user failed",
                status=status.HTTP_400_BAD_REQUEST
            )
        
    else:
        return Response({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
def privacy_policy(request):
    policy = PrivacyPolicy.objects.latest('updated_at')
    return JsonResponse({'content': policy.content})


class PasswordResetView(APIView):
    User = get_user_model()
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                reset_link = build_password_reset_link(user, request)
                send_mail(
                    '비밀번호 재설정 요청',
                    f'비밀번호를 재설정하려면 여기를 클릭하세요: {reset_link}',
                    'from@example.com',
                    [email],
                    fail_silently=False,
                )
                return Response({"message": "비밀번호 재설정 이메일이 전송되었습니다."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"message": "이 이메일을 가진 사용자가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        print(serializer.errors)
        return Response({"message" : "오류가 발생하였습니다."}, status=status.HTTP_400_BAD_REQUEST)

def build_password_reset_link(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    return request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.pk) + text_type(timestamp)

token_generator = TokenGenerator()

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
