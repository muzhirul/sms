from django.contrib import admin
from .models import *

# Register your models here.
class GradeAdmin(admin.ModelAdmin):
    list_display = ['name','start_mark','end_mark','point','status']
    
    class Meta:
        model = Grade
        
admin.site.register(Grade,GradeAdmin)