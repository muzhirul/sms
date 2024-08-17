from django.contrib import admin
from student.models import *
from fees.models import *
import admin_thumbnails


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','status','created_by','created_at']
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
    fields = ['version','session','class_name','group','section','roll','start_date','end_date','remarks','is_active','status','institution','branch']
    extra = 0

class ProcessStAttendanceDailyAdminTabularInline(admin.TabularInline):
    model = ProcessStAttendanceDaily
    fields = ['attn_date','shift','in_time','out_time','duration','attn_type','late_by_min','early_gone_by_min']
    extra = 0

class FeesTransactionAdminTabularInline(admin.TabularInline):
    model = FeesTransaction
    fields = ['fees_detail','payment_id','pay_method','pay_date','discount_type','discount_amt','fine_amt','fees_amt','pay_status']
    extra = 0

class StudentLeaveTransactionTabularInline(admin.TabularInline):
    model = StudentLeaveTransaction
    fields = ['start_date','end_date','app_status']
    extra = 0

@admin_thumbnails.thumbnail('photo')
class StudentAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Basic Information",{'fields':[('first_name','last_name','gender','category','shift'),
                                        ('email','dob','mobile_no','religion'),
                                        ('photo','photo_thumbnail','admission_date','blood_group'),
                                        ('birth_reg_scert_no','birth_cert_file'),]}),
        # ("Basic Information",{'fields':[('code','first_name','last_name','gender'),('email','dob','mobile_no','religion'),('photo','photo_thumbnail','admission_date','blood_group','Institution','status','is_online'),]}),
        ("Address",{'fields':[('present_address','permanent_address'),]})        
    ]
    list_display = ['student_no','first_name','last_name','dob','admission_date','blood_group','status','photo_thumbnail','std_status']
    search_fields = ['code','first_name','last_name','dob','admission_date','blood_group']
    list_filter = ['blood_group']

    save_as = True
    save_on_top = True
    list_per_page = 15

    inlines = [GuardianTabularInline,StudentEnrollTabularInline,ProcessStAttendanceDailyAdminTabularInline,StudentLeaveTransactionTabularInline,FeesTransactionAdminTabularInline]
    
    class Meta:
        model = Student

class ProcessStAttendanceDailyAdmin(admin.ModelAdmin):
    
    list_display = ['attn_date','shift','in_time','out_time','duration','attn_type','late_by_min','early_gone_by_min']

    class Meta:
        model = ProcessStAttendanceDaily

class StudentLeaveTransactionAdmin(admin.ModelAdmin):
    list_display = ['code','start_date','end_date','day_count','student_code','class_name','section','roll','app_status']

    class Meta:
        model = StudentLeaveTransaction

class StudentStatusTransactionAdmin(admin.ModelAdmin):
    list_display = ['code','student','reason','std_status','status']

    class Meta:
        model = StudentStatusTransaction



admin.site.register(Student,StudentAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(ProcessStAttendanceDaily,ProcessStAttendanceDailyAdmin)
admin.site.register(StudentLeaveTransaction,StudentLeaveTransactionAdmin)
admin.site.register(StudentStatusTransaction,StudentStatusTransactionAdmin)