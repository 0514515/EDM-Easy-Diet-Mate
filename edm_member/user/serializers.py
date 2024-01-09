from .models import User
from rest_framework import serializers
from .exceptions import UserAlreadyExistsException
from datetime import date
from django.utils import timezone

# 비밀번호 재설정용 Serializer
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return value

# 유저 정보 Serializer
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

# 회원가입 Serializer
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
    
    # 생일 검증
    def validate_birthdate(self, value):
        if value > date.today():
            raise serializers.ValidationError("미래의 날짜는 입력할 수 없습니다.")
        return value
    
    # 활동 레벨 검증
    def validate_active_level(self, value):
        if value not in ['1레벨 - 주 2회 미만, 움직임 거의 없는 사무직',
              '2레벨 - 주 3~4회 이하, 움직임 조금 있는 직종',
              '3레벨 - 주 5회 이하, 운송업 종사자',
              '4레벨 - 주 6회 이상, 인부 혹은 광부',
              '5레벨 - 운동 선수']:
            raise serializers.ValidationError("활동 수준은 1부터 5 사이의 값이어야 합니다.")
        return value
    
    # 신장 검증
    def validate_height(self, value):
        if value < 0:
            raise serializers.ValidationError("키는 0 이상이어야 합니다.")
        return value

    # 체중 검증
    def validate_weight(self, value):
        if value < 0:
            raise serializers.ValidationError("체중은 0 이상이어야 합니다.")
        return value
    
    # 다이터트 목적 검증
    def validate_diet_purpose(self, value):
        if value not in ['체중 감량', '체중 유지', '체중 증량']:
            raise serializers.ValidationError("유효한 다이어트 목적을 선택해주세요.")
        return value

    # 성별 검증
    def validate_gender(self, value):
        if value not in ['남자', '여자']:
            raise serializers.ValidationError("성별은 '남자' 혹은 '여자'로 입력해주세요.")
        return value
    
    # 비밀번호 검증
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("비밀번호는 8자 이상이어야 합니다.")
        return value
        
    # 검증을 통과한 값인 validated_data의 값만을 넣어줌.
    def create(self, validated_data):
        agreed_to_privacy_policy = validated_data['agreed_to_privacy_policy']
        
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            birthdate=validated_data['birthdate'],
            active_level=validated_data['active_level'],
            height=validated_data['height'],
            weight=validated_data['weight'],
            diet_purpose=validated_data['diet_purpose'],
            gender=validated_data['gender'],
            password=validated_data['password'],
        )

        if agreed_to_privacy_policy:
            user.agreed_to_privacy_policy = True
            user.privacy_policy_agreed_at = timezone.now()
            user.save()
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
            'gender',
            'password',
            'agreed_to_privacy_policy',  # 추가
            # uuid, created_at, updated_at은 회원가입 시 입력하지 않으므로 포함시키지 않음
        ]
       

# 로그인 Seriailizer
class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "password"
        ]
        
# 유저 정보 수정 Serializer
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "height",
            "weight",
            "active_level",
            "diet_purpose",
        ]