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
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetCompleteView,PasswordResetConfirmView

# 커스텀 response
def user_response(message="", display_message="",status=status.HTTP_400_BAD_REQUEST):
    return Response(
        {
            "message": message,
            "display_message": display_message
        },
        status=status
    )
    
# 이메일 사용 확인 View
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
    permission_classes = [AllowAny] # 회원 가입은 토큰 없이도 가능해야하기에 토큰 없는 접근 허용
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

# 로그인
class Login(APIView):
    serializer_class = LoginUserSerializer
    permission_classes = [AllowAny] # 로그인은 토큰 없이도 가능해야하기에 토큰 없는 접근 허용
    
    def post(self, request):
        print(request)
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

#회원 정보 조회, 수정, 삭제
@api_view(['GET','PATCH','POST'])
@permission_classes([IsAuthenticated])
def user_info(request):
    
    # 토큰 검증과 토큰 속 uuid 디코딩
    jwt_authenticator = JWTAuthentication()
    try:
        validated_token = jwt_authenticator.get_validated_token(request.headers.get('Authorization').split(' ')[1])
        uuid = jwt_authenticator.get_user(validated_token).uuid

    except Exception as e:
        return Response({"message": "Invalid token"}, status=status.HTTP_403_FORBIDDEN)
    
    # 회원 정보 수정
    if request.method=='PATCH':
        try:
            user = User.objects.filter(uuid=uuid).first()
            data = request.data
            
            # 키와 몸무게가 값이 없을 경우 유저의 기존 값으로 대체
            if data['height']=='':
                data['height']=user.height
            if data['weight']=='':
                data['weight']=user.weight
            data = UpdateUserSerializer(request.data).data
            
            
            # 회원이 없는 경우
            if not user:
                print("user is not exists")
                return user_response(
                    message="user is not exists",
                    display_message="존재하지 않는 회원입니다.",
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Update 완료한 유저를 Serialize
            serializer = UpdateUserSerializer(user, data=data, partial=True)
            print(serializer)
            
            # Serializer된 값 검증
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
    
    
    # 회원 삭제
    # 회원 삭제에 email과 비밀번호 확인 때문에 body로 정보를 전송하므로
    # DELETE가 아닌 POST로 처리
    elif request.method=='POST':
        
        try:
            email = request.data['email']
            password = request.data['password']
            
            # 보낸 토큰 속 uuid로 사용자를 조회
            user1 = User.objects.filter(uuid=uuid).first()
            # body에 있는 email을 조회
            user2 = User.objects.filter(email=email).first()
            
            # 토큰 속 uuid의 유저를 찾을 수 없을 경우
            if not user1:
                print("user is not exists")
                return user_response(
                    message="user is not exists",
                    display_message="존재하지 않는 회원입니다.",
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            
            # 토큰 속 uuid 유저의 email과 body 속 email이 다를 경우
            # (내 이메일을 올바르게 입력하지 않았을 경우)        
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
            
            # 삭제   
            if (email==user1.email) and check_password(password, user1.password):
                user1.delete()
                return user_response(
                    display_message="회원탈퇴에 성공하였습니다.",
                    message="delete user success",
                    status=status.HTTP_200_OK
                )
            
            # 모든 경우가 아닐 때
            return user_response(
                display_message="회원 삭제에 실패하였습니다.",
                message="delete user failed",
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # 예외 발생시
        except:
            return user_response(
                display_message="회원 삭제에 실패하였습니다.",
                message="delete user failed",
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # 회원 정보 조회
    elif request.method=='GET':
        try:
            data = UpdateUserSerializer(request.data).data
            
            user = User.objects.filter(uuid=uuid).first()
            
            # 회원 찾을 수 없을 때
            if not user:
                print("user is not exists")
                return user_response(
                    message="user is not exists",
                    display_message="존재하지 않는 회원입니다.",
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            serializer = UpdateUserSerializer(user, data=data, partial=True)
            
            # serializer 유효성 검증 올바를 때
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "user" : UserInfoSerializer(user).data,
                }
                )
                
            # 올바르지 않을 때
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # 기타 예외 발생하였을 때
        except:
            return user_response(
                display_message="회원 조회에 실패하였습니다.",
                message="search user failed",
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # HTTP 메소드 종류 잘못되었을 때
    else:
        return Response({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
# 가장 최근의 개인정보 처리방침 조회
def privacy_policy(request):
    policy = PrivacyPolicy.objects.latest('updated_at')
    return JsonResponse({'content': policy.content})


# 비밀번호 재설정 완료 페이지 View
class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'reset_password_complete.html'
    

# 비밀번호 재설정 이메일 요청 View
class PasswordResetView(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"http://edm.japaneast.cloudapp.azure.com/api/reset/{uid}/{token}"
            send_mail(
                "비밀번호 재설정 요청",
                f"비밀번호를 재설정하려면 다음 링크를 클릭하세요: {reset_link}",
                "from@example.com",
                [email],
                fail_silently=False,
            )
            return Response({"message": "비밀번호 재설정 링크가 발송되었습니다."}, status=status.HTTP_200_OK)
        
        # 이메일 주소를 찾을 수 없을 때
        except User.DoesNotExist:
            return Response({"message": "이 이메일 주소를 가진 사용자가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        # 기타 예외
        except Exception as e:
            return Response({"message": "비밀번호 재설정에 실패하였습니다."}, status=status.HTTP_400_BAD_REQUEST)