from django.contrib import admin
from admission.models import *
import admin_thumbnails
# Register your models here.

class AdminArea(admin.AdminSite):
    site_header = 'School Management System'

@admin_thumbnails.thumbnail('photo')
class GuardianTabularInline(admin.TabularInline):
    model = Guardian
    fields = ['first_name','last_name','mobile_no','relation','gender','ocupation','nid','photo','photo_thumbnail','is_guardian','status']
    extra = 0

class AdmissionTestResultTabularInline(admin.TabularInline):
    model = AdmissionTestResult
    fields =['subject','mark','institution','status']
    extra = 0
@admin_thumbnails.thumbnail('photo')
class AdmissionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Basic Information",{'fields':[('code','first_name','last_name','gender'),('email','dob','mobile_no','religion'),('photo','photo_thumbnail','admission_date','blood_group','Institution','status','is_online'),]}),
        ("Address",{'fields':[('present_address','permanent_address'),]})        
    ]
    list_display = ['code','first_name','last_name','dob','admission_date','blood_group','status','photo_thumbnail']
    search_fields = ['code','first_name','last_name','dob','admission_date','blood_group']
    list_filter = ['blood_group']

    # save_as = True
    save_on_top = True
    list_per_page = 15

    inlines = [GuardianTabularInline,AdmissionTestResultTabularInline]
    
    class Meta:
        model = Admission

# admin.site.register(Admission,AdmissionAdmin)
