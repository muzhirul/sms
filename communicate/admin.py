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

# class SmsSendSetupAdminForm(forms.ModelForm):
#     class Meta:
#         model = SmsSendSetup
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
        
#         if 'template' in self.data:
#             try:
#                 template_id = int(self.data.get('template'))
#                 template = SmsTemplate.objects.get(id=template_id)
#                 self.initial['title'] = template.title
#                 self.initial['message_body'] = template.message_body
#             except (ValueError, TypeError, SmsTemplate.DoesNotExist):
#                 pass
#         elif self.instance and self.instance.template:
#             self.initial['title'] = self.instance.template.title
#             self.initial['message_body'] = self.instance.template.message_body

class SmsSendSetupAdmin(admin.ModelAdmin):
    filter_horizontal = ('group', 'individual','class_section')
    # form = SmsSendSetupAdminForm
    class Meta:
        model = SmsSendSetup

admin.site.register(SmsTemplate,SmsTemplateAdmin)
admin.site.register(NoticeBoard,NoticeBoardAdmin)
admin.site.register(SmsSendSetup,SmsSendSetupAdmin)