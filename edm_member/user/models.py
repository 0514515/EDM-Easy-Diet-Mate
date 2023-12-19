from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
import uuid

# 유저 CRUD 쿼리 정의
class UserManager(BaseUserManager):
    def create_user(self, email, name, birthdate, active_level, height, weight, diet_purpose, gender, password=None):
        if not email:
            raise ValueError('must have user email')
        if not name:
            raise ValueError('must have user name')
        if not birthdate:
            raise ValueError('must have user birthdate')
        if not active_level:
            raise ValueError('must have user active level')
        if not height:
            raise ValueError('must have user height')
        if not weight:
            raise ValueError('must have user weight')
        if not diet_purpose:
            raise ValueError('must have user diet_purpose')
        if not gender:
            raise ValueError('must have user gender')
        
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            birthdate = birthdate,
            active_level = active_level,
            height = height,
            weight = weight,
            diet_purpose = diet_purpose,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
# 회원 모델
class User(AbstractBaseUser):
    active_level_choice = [
        ('level 1','1레벨'),
        ('level 2','2레벨'),
        ('level 3','3레벨'),
        ('level 4','4레벨'),
        ('level 5','5레벨'),
        ]
    diet_purpose_choice = [
        ('loss_weight','체중 감량'),
        ('keep_weight','체중 유지'),
        ('gain_weight','체중 증량'),
    ]
    gender_choice =[
        ('man','남자'),
        ('woman','여자')
    ]
    
    # User 모델의 필드
    id = models.AutoField(primary_key=True)
    email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
    name = models.CharField(default='', max_length=10, null=False, blank=False)
    birthdate = models.DateField(null=False)
    active_level = models.CharField(
        max_length=7,
        null=False,
        blank=False,
        choices=active_level_choice,
        default='level 1',
        )
    height = models.CharField(default=0, null=False, blank=False, max_length=7)
    weight = models.CharField(default=0, null=False, blank=False, max_length=7)
    diet_purpose= models.CharField(
        max_length=11,
        null=False,
        blank=False,
        choices=diet_purpose_choice,
        default='체중 유지',
        )
    gender = models.CharField(
        max_length=5,
        null=False,
        blank=False,
        choices=gender_choice,
        default='남자',
        )
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    
    created_at = models.DateTimeField(editable=False,auto_now_add=True)
    updated_at = models.DateTimeField(editable=False,auto_now=True)
    
    # User 모델의 필수 필드
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    # manager
    manager = UserManager()
    
    # username 필드 정의
    USERNAME_FIELD = 'email'
    
    # 필수 작성 필드
    REQUIRED_FIELDS = [
        'name',
        ]
    
    def __str__(self):
        return self.name