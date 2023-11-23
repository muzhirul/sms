from django.contrib import admin
from student.models import *
import admin_thumbnails


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','status']
    save_on_top = True
    list_per_page = 15

    class Meta:
        model = Category



# Register your models here.
@admin_thumbnails.thumbnail('photo')
class GuardianTabularInline(admin.TabularInline):
    model = Guardian
    fields = ['first_name','last_name','mobile_no','relation','gender','occupation','nid','photo','photo_thumbnail','is_guardian']
    extra = 0

class StudentEnrollTabularInline(admin.TabularInline):
    model = StudentEnroll
    fields = ['version','session','class_name','section','roll','start_date','end_date','remarks']
    extra = 0

@admin_thumbnails.thumbnail('photo')
class StudentAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Basic Information",{'fields':[('first_name','last_name','gender'),('email','dob','mobile_no','religion'),('photo','photo_thumbnail','admission_date','blood_group'),]}),
        # ("Basic Information",{'fields':[('code','first_name','last_name','gender'),('email','dob','mobile_no','religion'),('photo','photo_thumbnail','admission_date','blood_group','Institution','status','is_online'),]}),
        ("Address",{'fields':[('present_address','permanent_address'),]})        
    ]
    list_display = ['student_no','first_name','last_name','dob','admission_date','blood_group','status','photo_thumbnail']
    search_fields = ['code','first_name','last_name','dob','admission_date','blood_group']
    list_filter = ['blood_group']

    # save_as = True
    save_on_top = True
    list_per_page = 15

    inlines = [GuardianTabularInline,StudentEnrollTabularInline]
    
    class Meta:
        model = Student

admin.site.register(Student,StudentAdmin)
admin.site.register(Category,CategoryAdmin)