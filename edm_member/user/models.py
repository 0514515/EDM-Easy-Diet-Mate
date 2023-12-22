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
    
    def create_superuser(self, email, password, name):
        user = self.create_user(
            email,
            name=name,
            password=password,
            active_level='level 1',
            height='0',
            weight='0',
            birthdate=timezone.now,
            diet_purpose='loss weight',
            gender='남자',
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
    

# 회원 모델
class User(AbstractBaseUser):
    active_level_choice = [
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
        ]
    diet_purpose_choice = [
        ('체중 감량','체중 감량'),
        ('체중 유지','체중 유지'),
        ('체중 증량','체중 증량'),
    ]
    gender_choice =[
        ('남자','남자'),
        ('여자','여자')
    ]
    
    # User 모델의 필드
    id = models.AutoField(primary_key=True)
    email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
    name = models.CharField(default='', max_length=10, null=False, blank=False)
    birthdate = models.DateField(default=timezone.now, null=False)
    active_level = models.CharField(
        max_length=7,
        null=False,
        blank=False,
        choices=active_level_choice,
        default='level 1',
        )
    height = models.SmallIntegerField(default=0, null=False, blank=False,)
    weight = models.SmallIntegerField(default=0, null=False, blank=False,)
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
    
    # objects
    objects = UserManager()
    
    # username 필드 정의
    USERNAME_FIELD = 'email'
    
    # 필수 작성 필드
    REQUIRED_FIELDS = [
        'name',
        ]
    
    def __str__(self):
        return self.name
    
    # 기본 유저 모델 admin용
    def has_perm(self, perm, obj=None):
        return True
    
    # 기본 유저 모델 admin용
    def has_module_perms(self, app_label):
        return True
    
    # 기본 유저 모델 admin용
    @property
    def is_staff(self):
        return self.is_admin