from django.contrib import admin
from board.models import *
from user.models import *
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from subscribe.models import *
from django.contrib.admin.views.main import ChangeList



# FAQ 관리
class FAQAdmin(admin.ModelAdmin):
    list_display = ['title', 'content']     # FAQ 관리에서 보여질 필드
    search_fields = ['title', 'content']    # 검색 기준 필드

# 공지 관리
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'posted_on']    # 공지에서 보여질 필드
    search_fields = ['title', 'content']                # 검색 기준 필드
    list_filter = ['posted_on']  # 필터 옵션 추가

# 회원 관리
class UserAdmin(BaseUserAdmin):
    change_password_form = AdminPasswordChangeForm  # 비밀번호 변경 폼 추가
    
    model = User    # 다루는 모델
    list_display = ('email', 'name', 'is_active', 'is_admin')   # 회원 목록에서 보여질 필드
    list_filter = ('is_active', 'is_admin') 
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'birthdate', 'active_level', 'height', 'weight', 'diet_purpose', 'gender',)}),  
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',) # 검색 기준 필드
    ordering = ('email',) # 정렬
    filter_horizontal = ()
    
# 카드뉴스 관리
class CardNewsAdmin(admin.ModelAdmin):
    list_display = ['title']  # 관리자 페이지에서 보여질 필드
    search_fields = ['title']  # 검색 가능한 필드
    
# 구독 관리
class SubscribeAdmin(admin.ModelAdmin):
    # 사용자의 이메일과 이름을 조합
    def subscribe_from_info(self, obj):
        return f"{obj.subscribe_from.email} <{obj.subscribe_from.name}>"
    subscribe_from_info.short_description = '구독하는 사용자'

    def subscribe_to_info(self, obj):
        return f"{obj.subscribe_to.email} <{obj.subscribe_to.name}>"
    subscribe_to_info.short_description = '구독받는 사용자'

    list_display = ('subscribe_from_info', 'subscribe_to_info', 'created_at')   # 구독 목록에서 보여질 필드
    
    
# 정책 내용 관리
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ['updated_at']
    search_fields = ['content']

# 1대1 문의 답변 페이지 인라인
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0  # 추가 폼을 보여주지 않습니다.

# 1대1 문의 관리
class AskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')  # 관리자 목록에 표시할 필드
    search_fields = ['title', 'content']  # 검색 가능한 필드
    inlines = [AnswerInline]    # 1대1문의에서 즉시 답변을 달 수 있게 설정
    ordering = ['-created_at']  # 가장 최근에 올라온 문의부터 출력
    

# 1대1 문의 답변 관리
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['ask', 'content', 'created_at']


# 관리자 페이지에 추가
admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(CardNews, CardNewsAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Ask, AskAdmin)
admin.site.register(Answer,AnswerAdmin)