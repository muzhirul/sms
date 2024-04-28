from django.contrib import admin
from .models import *

# Register your models here.
class NoticeBoardAdmin(admin.ModelAdmin):
    list_display = ['title','notice_date','publish_date','is_active','created_at','status']
    search_fields = ['title']

    class Meta:
        model = NoticeBoard

admin.site.register(NoticeBoard,NoticeBoardAdmin)