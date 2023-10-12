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
    list_display = ['staff_id','first_name','last_name']
    fieldsets = [
        ("Basic Information",{'fields':[('first_name','last_name','gender'),('email','dob','mobile_no','religion'),('photo','photo_thumbnail','blood_group'),]}),
        ("Address",{'fields':[('present_address','permanent_address'),]}),
        ("Assignment",{'fields':[('department','designation','shift'),]})        
    ]
    
    class Meta:
        model = Staff
    
    inlines = [EducationTabularInline]

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name','dept_ord']
    fields = ['name','dept_ord']

    class Meta:
        model = Department

class DesignationAdmin(admin.ModelAdmin):
    list_display = ['name','desgi_ord']
    fields = ['name','desgi_ord']

    class Meta:
        model = Designation
        
class StaffShiftAdmin(admin.ModelAdmin):
    list_display = ['code','name','start_time','end_time','status']
    fields = ['name','start_time','end_time','remarks']
    class Meta:
        model = StaffShift



admin.site.register(Staff,StaffAdmin)
admin.site.register(Designation,DesignationAdmin)
admin.site.register(Department,DepartmentAdmin)
admin.site.register(StaffShift,StaffShiftAdmin)