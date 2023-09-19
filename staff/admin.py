from django.contrib import admin
from staff.models import *
import admin_thumbnails

# Register your models here.
class EducationTabularInline(admin.TabularInline):
    model = Education
    fields = ['institution_name','registration_no','title','board','start_date','end_date','passing_year','result','result_out_of','remarks','status']
    extra = 1
    
@admin_thumbnails.thumbnail('photo')
class StaffAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Basic Information",{'fields':[('first_name','last_name','gender'),('email','dob','mobile_no','religion'),('photo','photo_thumbnail','blood_group'),]}),
        ("Address",{'fields':[('present_address','permanent_address'),]})        
    ]
    
    class Meta:
        model = staff
    
    inlines = [EducationTabularInline]



admin.site.register(staff,StaffAdmin)
admin.site.register(Designation)
admin.site.register(Department)