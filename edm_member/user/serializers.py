from .models import User
from rest_framework import serializers
from .exceptions import UserAlreadyExistsException
from datetime import date

class UserInfoSerializer(serializers.ModelSerializer):
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
            'gender',
            'uuid',
        ]

class CreateUserSerializer(serializers.ModelSerializer):
    
    def validate_email(self, value):
    # 이메일 형식 검증
        if not value or value.strip() == '':
            raise serializers.ValidationError("이메일 주소는 필수입니다.")
        if not value or "@" not in value:
            raise serializers.ValidationError("유효한 이메일 주소를 입력해주세요.")
        # 이메일 중복 검증
        if User.objects.filter(email=value):
            raise serializers.ValidationError("이미 사용 중인 이메일입니다.")
        return value
    
    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("이름을 입력해주세요.")
        # 이름 길이 제한 검증
        if len(value) > 10:
            raise serializers.ValidationError("이름은 10자 이내로 입력해주세요.")
        return value
    
    def validate_birthdate(self, value):
        if value > date.today():
            raise serializers.ValidationError("미래의 날짜는 입력할 수 없습니다.")
        return value
    
    def validate_active_level(self, value):
        if value not in ['1', '2', '3', '4', '5']:
            raise serializers.ValidationError("활동 수준은 1부터 5 사이의 값이어야 합니다.")
        return value
    
    def validate_height(self, value):
        if value < 0:
            raise serializers.ValidationError("키는 0 이상이어야 합니다.")
        return value

    def validate_weight(self, value):
        if value < 0:
            raise serializers.ValidationError("체중은 0 이상이어야 합니다.")
        return value
    
    def validate_diet_purpose(self, value):
        if value not in ['체중 감량', '체중 유지', '체중 증량']:
            raise serializers.ValidationError("유효한 다이어트 목적을 선택해주세요.")
        return value

    def validate_gender(self, value):
        if value not in ['남자', '여자']:
            raise serializers.ValidationError("성별은 '남자' 혹은 '여자'로 입력해주세요.")
        return value
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("비밀번호는 8자 이상이어야 합니다.")
        return value
        
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
       

       
class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "password"
        ]
        
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "height",
            "weight",
            "active_level",
            "diet_purpose",
        ]