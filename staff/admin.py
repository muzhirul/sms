from django.contrib import admin
from staff.models import *
import admin_thumbnails

# Register your models here.
class EducationTabularInline(admin.TabularInline):
    model = Education
    fields = ['institution_name','registration_no','title','edu_board','start_date','end_date','passing_year','result','result_out_of','remarks','status']
    extra = 1

class PayrollTabularInline(admin.TabularInline):
    model = StaffPayroll
    fields = ['gross','start_date','end_date','contract_type','is_active','remarks','status']
    extra = 1

class BankAccountDetailsTabularInline(admin.TabularInline):
    model = StaffBankAccountDetails
    fields = ['account_title','account_number','bank_name','branch_name','is_active','remarks','status']
    extra = 1

class StaffSocialMediaTabularInline(admin.TabularInline):
    model = StaffSocialMedia
    fields = ['name','username','url','status']
    extra = 1

class StaffLeaveTabulrInline(admin.TabularInline):
    model = StaffLeave
    fields = ['leave_type','leave_days','taken_days','start_date','end_date','is_active','status']
    extra = 1

class ProcessAttendanceDailyAdminTabularInline(admin.TabularInline):
    model = ProcessAttendanceDaily
    fields = ['attn_date','shift','in_time','out_time','duration','attn_type','late_by_min','early_gone_by_min']
    extra = 0

    
@admin_thumbnails.thumbnail('photo')
class StaffAdmin(admin.ModelAdmin):
    list_display = ['staff_id','first_name','last_name']
    fieldsets = [
        ("Basic Information",{'fields':[('first_name','last_name','gender','religion'),('email','dob','mobile_no','emergency_number','nid'),('photo','photo_thumbnail','blood_group','marital_status'),]}),
        ("Address",{'fields':[('present_address','permanent_address'),]}),
        ("Assignment",{'fields':[('doj','role','department','designation','shift','status'),]})        
    ]
    
    class Meta:
        model = Staff
    
    inlines = [EducationTabularInline,PayrollTabularInline,BankAccountDetailsTabularInline,StaffSocialMediaTabularInline,StaffLeaveTabulrInline,ProcessAttendanceDailyAdminTabularInline]

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

class ProcessAttendanceDailyAdmin(admin.ModelAdmin):
    list_display = ['attn_date','staff_code','in_time','out_time','attn_type']
    class Meta:
        model = ProcessAttendanceDaily

class StaffLeaveAppHistoryTabularInline(admin.TabularInline):
    model = StaffLeaveAppHistory
    fields = ['approve_group','approve_by','app_status','remarks','is_active','institution','branch','status']
    extra = 0


class StaffLeaveTransactionAdmin(admin.ModelAdmin):
    list_display = ['code','leave_type','start_date','end_date','day_count']
    
    class Meta:
        model = StaffLeaveTransaction
    
    inlines = [StaffLeaveAppHistoryTabularInline]



admin.site.register(Staff,StaffAdmin)
admin.site.register(Designation,DesignationAdmin)
admin.site.register(Department,DepartmentAdmin)
admin.site.register(StaffShift,StaffShiftAdmin)
admin.site.register(ProcessAttendanceDaily,ProcessAttendanceDailyAdmin)
admin.site.register(StaffLeaveTransaction,StaffLeaveTransactionAdmin)
admin.site.register(StaffLeaveAppHistory)