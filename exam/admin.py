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
        
class ExamRoutineAdmin(admin.ModelAdmin):
    class Meta:
        model = ExamRoutine

admin.site.register(Grade,GradeAdmin)
admin.site.register(ExamName, ExamNameAdmin)
admin.site.register(ExamRoutine, ExamRoutineAdmin)