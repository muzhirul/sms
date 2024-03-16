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
    list_display = ['start_time','day','end_time','duration']
    class Meta:
        model = ExamRoutine

class ExamRoutineDtlAdmin(admin.TabularInline):
    model = ExamRoutineDtl
    fields = ['exam_date','subject','room','start_time','end_time','teacher','status','institution','branch']
    extra = 0

class ExamRoutineMstAdmin(admin.ModelAdmin):
    list_display = ['class_name','section','group','session','version','status','institution','branch']
    class Meta:
        model = ExamRoutineMst
    inlines = [ExamRoutineDtlAdmin]

admin.site.register(Grade,GradeAdmin)
admin.site.register(ExamName, ExamNameAdmin)
admin.site.register(ExamRoutine, ExamRoutineAdmin)
admin.site.register(ExamRoutineMst,ExamRoutineMstAdmin)