from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from .models import Subscribe
from django.core.exceptions import *
from django.db.utils import IntegrityError
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
            
            try:
                user1 = User.objects.filter(uuid=data["subscribe_from"]).first()
            except ValidationError as e:
                print(type(e),e)
                return Response(
                    {
                        "message" : "subscriber not found",
                        "display_message" : "구독자를 찾을 수 없습니다."
                    }
                )
                
            try:
                user2 = User.objects.filter(uuid=data["subscribe_to"]).first()
            except ValidationError as e:
                print(type(e),e)
                return Response(
                    {
                        "message" : "subscribe target not found",
                        "display_message" : "피구독자를 찾을 수 없습니다."
                    }
                )                    
                
            if user1 and user2:
                try:
                    check_subscribe = Subscribe.objects.filter(subscribe_from = user1,subscribe_to = user2).first()
                    
                    subscribe = Subscribe.objects.create_subscribe(user1,user2)
                
                except IntegrityError as e:
                    print(type(e),e)
                    return Response(
                        {
                            "message":"this subscribe already exists",
                            "display_message":"이미 구독하고 있습니다."
                        }
                    )
                except Exception as e:
                    print(type(e),e)
                    return Response(
                        {
                            "message":"user are ok but we can't create subscribe",
                            "display_message":"구독 중 에러가 발생하였습니다."
                        }
                    )
                return Response(
                    {
                        "message" : "subscribe success",
                        "display_message" : "구독에 성공하였습니다."
                    }, status=status.HTTP_200_OK
                )
            
        except Exception as e:
            print("error",type(e),e)
            return Response(
                {
                    "message":"error",
                    "display_message" : "에러가 발생하였습니다."
                }, status=status.HTTP_400_BAD_REQUEST
            )
            
    elif request.method=='DELETE':
        try:
            
            print('delete')
        except:
            print('delete except')
            
    else:
        return Response({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)