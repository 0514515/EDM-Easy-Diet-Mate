from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from .models import Subscribe
# Create your views here.

@api_view(['GET','POST','DELETE'])
def subscribe(request):
    if request.method=='GET':
        try:
            print('get')
        except:
            print('except')
            
    elif request.method=='POST':
        try:
            data = request.data
            
            print(data)
            
            user1 = User.objects.filter(uuid=data["subscribe_from"]).first()
            user2 = User.objects.filter(uuid=data["subscribe_to"]).first()
            
            if not user1:
                return Response(
                    {
                        "message" : "subscriber not found",
                        "display_message" : "구독자를 찾을 수 없습니다."
                    }
                )
            if not user2:
                return Response(
                    {
                        "message" : "subscribe user not found",
                        "display_message" : "구독할 유저를 찾을 수 없습니다."
                    }
                )
                
                
            if user1 and user2:
                return Response(
                    {
                        "message" : "subscribe success",
                        "display_message" : "post"
                    }, status=status.HTTP_200_OK
                )
            
        except:
            print("error")
            # return Response(
            #     {
            #         "message" : "에러가 발생하였습니다."
            #     }, status=status.HTTP_400_BAD_REQUEST
            # )
            
    elif request.method=='DELETE':
        try:
            
            print('delete')
        except:
            print('delete except')
            
    else:
        return Response({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)