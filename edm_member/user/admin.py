from django.contrib import admin
from board.models import FAQ, Notice

class FAQAdmin(admin.ModelAdmin):
    list_display = ['title', 'content']  # 리스트에서 보여줄 필드
    search_fields = ['title', 'content']  # 검색할 수 있는 필드

class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'posted_on']
    search_fields = ['title', 'content']
    list_filter = ['posted_on']  # 필터 옵션 추가

admin.site.register(FAQ, FAQAdmin)
admin.site.register(Notice, NoticeAdmin)