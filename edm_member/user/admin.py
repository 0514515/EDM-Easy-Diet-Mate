from django.contrib import admin
from board.models import *
from .models import *
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class FAQAdmin(admin.ModelAdmin):
    list_display = ['title', 'content']  # 리스트에서 보여줄 필드
    search_fields = ['title', 'content']  # 검색할 수 있는 필드

class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'posted_on']
    search_fields = ['title', 'content']
    list_filter = ['posted_on']  # 필터 옵션 추가

class UserAdmin(BaseUserAdmin):
    change_password_form = AdminPasswordChangeForm
    
    model = User
    list_display = ('email', 'name', 'is_active', 'is_admin')
    list_filter = ('is_active', 'is_admin')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'birthdate', 'active_level', 'height', 'weight', 'diet_purpose', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    
class CardNewsAdmin(admin.ModelAdmin):
    list_display = ['title']  # 관리자 페이지에서 보여질 필드
    search_fields = ['title']  # 검색 가능한 필드

admin.site.register(User, UserAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(CardNews, CardNewsAdmin)
admin.site.register(PrivacyPolicy)