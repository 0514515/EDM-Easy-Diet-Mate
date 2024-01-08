from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from .models import Subscribe
from django.core.exceptions import *
from subscribe.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
import uuid
# Create your views here.

# UUID 검증
def is_valid_uuid(uuid_to_test, version=4):
    try:
        # 하이픈을 제거합니다
        uuid_to_test = uuid_to_test.replace('-', '')
        # 문자열 길이를 체크합니다 (하이픈이 제거된 UUID v4는 32글자여야 합니다)
        if len(uuid_to_test) != 32:
            return False
        # UUID 객체를 생성하여 형식을 검증합니다
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    # 객체를 문자열로 변환하여 입력된 UUID와 비교합니다
    return uuid_obj.hex == uuid_to_test

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def subscribe(request):
    user = request.user

    # 나의 구독 리스트 조회
    if request.method == 'GET':
        subscriptions = Subscribe.objects.filter(subscribe_from=user)
        serializer = SubscribeSerializer(subscriptions, many=True)

        # 각 구독 객체에서 'subscribe_to' 필드의 값을 추출하여 리스트에 추가합니다.
        values_list = [str(subscription['subscribe_to']).replace('-', '') for subscription in serializer.data]

        return Response(values_list)
    
    elif request.method == 'POST':
        user = request.user
        email = request.data.get('email')

        # 이메일과 이름으로 사용자 찾기
        try:
            subscribe_to_user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': "User not found", "display_message": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 자기 자신을 구독하는 것을 방지
        if user.uuid == subscribe_to_user.uuid:
            return Response({
                "message": "Cannot subscribe to oneself",
                "display_message": "자기 자신을 구독할 수 없습니다."
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # 구독 존재 체크
        if Subscribe.objects.filter(subscribe_from=user, subscribe_to=subscribe_to_user).exists():
            return Response({
                "message": "Subscribe already exists",
                "display_message": "이미 구독하고 있습니다."
            }, status=status.HTTP_400_BAD_REQUEST)

        # 구독 생성
        subscribe_data = {'subscribe_from': user.uuid, 'subscribe_to': subscribe_to_user.uuid}
        serializer = SubscribeSerializer(data=subscribe_data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "subscribe": serializer.data,
                "message": "Subscribe is success",
                "display_message": "구독이 완료되었습니다."
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 구독한 사람의 이름 조회
@api_view(['GET'])
def get_user_name(request, uuid):
    try:
        # 요청을 보낸 사용자 (토큰 소유자)
        request_user = request.user

        # Path parameter로 받은 UUID의 사용자
        target_user = User.objects.filter(uuid=uuid).first()

        # 두 사용자 간의 구독 관계 확인
        if not Subscribe.objects.filter(subscribe_from=request_user, subscribe_to=target_user).exists():
            return Response({'message': 'No subscription found',"display_message":"구독이 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 구독 관계가 있는 경우, 이름 반환
        serializer = UserNameSerializer(target_user)
        return Response(serializer.data)

    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

# 구독 삭제
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_subscription(request, uuid):
    # User (from token)
    request_user = request.user

    # UUID of the subscribed person (from path parameter)
    target_user_uuid = uuid

    # Check if subscription exists
    try:
        subscription = Subscribe.objects.get(subscribe_from=request_user, subscribe_to__uuid=target_user_uuid)
    except Subscribe.DoesNotExist:
        return Response({'message': 'Subscription not found', "display_message": "구독이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

    # Delete the subscription
    subscription.delete()

    # Return a success response
    return Response({'message': 'Subscription deleted successfully', "display_message": "구독이 삭제되었습니다."}, status=status.HTTP_200_OK)