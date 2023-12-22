from .models import User
from rest_framework import serializers

class UserCreateSerializer(serializers.ModelSerializer):
    # 검증을 통과한 값인 validated_data의 값만을 넣어줌.
    def create(self, validated_data):
       user = User.objects.create_user(
           email = validated_data['email'],
           name = validated_data['name'],
           birthdate = validated_data['birthdate'],
           active_level = validated_data['active_level'],
           height = validated_data['height'],
           weight = validated_data['weight'],
           diet_purpose = validated_data['diet_purpose'],
           gender = validated_data['gender'],
           password = validated_data['password'],
       )
       return user
   
    class Meta:
       model = User
       fields = [
           'email',
           'name',
           'birthdate',
           'active_level',
           'height',
           'weight',
           'diet_purpose',
           'password',
           'gender',
           'uuid',
           'created_at',
           'updated_at',
           ]
       
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "password"
        ]
        
class DeleteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "password"
        ]