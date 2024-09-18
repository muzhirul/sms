from django.contrib import admin
from .models import *
from django import forms 

# Register your models here.
class NoticeBoardAdmin(admin.ModelAdmin):
    list_display = ['title','notice_date','publish_date','is_active','created_at','status']
    search_fields = ['title']

    class Meta:
        model = NoticeBoard

class SmsTemplateAdmin(admin.ModelAdmin):
    list_display = ['title','message_body','is_active','status','created_by']
    search_fields = ['title']

    class Meta:
        model = SmsTemplate

class SmsEmailLogAttachmentInline(admin.TabularInline):
    model = SmsEmailLogAttachment 
    extra = 1

class SmsEmailLogAdmin(admin.ModelAdmin):
    list_display = ['subject','email','sms','is_active','status','created_by','created_at']
    search_fields = ['subject']
    
    inlines = [SmsEmailLogAttachmentInline]
    class Meta:
        model = SmsEmailLog


admin.site.register(SmsTemplate,SmsTemplateAdmin)
admin.site.register(NoticeBoard,NoticeBoardAdmin)
admin.site.register(SmsEmailLog,SmsEmailLogAdmin)
