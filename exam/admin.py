from django.contrib import admin
from .models import *

# Register your models here.
class GradeAdmin(admin.ModelAdmin):
    list_display = ['name','start_mark','end_mark','point','status']
    
    class Meta:
        model = Grade
        
class ExamNameAdmin(admin.ModelAdmin):
    list_display = ['name','sl_no','session']
    
    class Meta:
        model = ExamName

admin.site.register(Grade,GradeAdmin)
admin.site.register(ExamName, ExamNameAdmin)