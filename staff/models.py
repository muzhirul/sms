from django.db import models
from institution.models import Institution, Branch
from setup_app.models import EducationBoard
from django_userforeignkey.models.fields import UserForeignKey
from setup_app.models import *
from account.models import *
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from datetime import datetime,date, time
from hrms.models import *
import datetime
from authentication.models import Authentication
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models import F
from django.db.models import Q
# Create your models here.

def validate_pdf_file_size(value):
    if value.size > 2 * 1024 * 1024:  # 20MB in bytes
        raise ValidationError('File size cannot exceed 2MB.')

def staff_no():
    last_guardian_no = Staff.objects.all().order_by('staff_id').last()
    if not last_guardian_no or last_guardian_no.staff_id is None:
        return '99' + str(datetime.date.today().year) + str(datetime.date.today().month).zfill(2) + '00'
    guardian_num = str(last_guardian_no.staff_id)[-2:]
    guardian_num_int = int(guardian_num)
    new_guardian_num = guardian_num_int + 1
    new_gd_num = '99' + str(str(datetime.date.today().year)) + str(datetime.date.today().month).zfill(2) + str(new_guardian_num).zfill(2)
    return new_gd_num 

def staff_shift_code():
    last_shift_no = StaffShift.objects.all().order_by('code').last()
    if not last_shift_no or last_shift_no.code is None:
        return 'SHIFT'+'000'
    guardian_num = last_shift_no.code[-3:]
    guardian_num_int = int(guardian_num)
    new_guardian_num = guardian_num_int + 1
    new_gd_num = 'SHIFT'+ str(new_guardian_num).zfill(3)
    return new_gd_num 

class Designation(models.Model):
    code = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    desgi_ord = models.IntegerField(blank=True, null=True, verbose_name='Designation Order')
    Institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='designation_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='designation_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sta_designation'

    def __str__(self):
        return str(self.name)

class Department(models.Model):
    code = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    dept_ord = models.IntegerField(blank=True, null=True, verbose_name='Department Order')
    Institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='department_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='department_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sta_department'

    def __str__(self):
        return str(self.name)

class StaffShift(models.Model):
    code = models.CharField(max_length=20,blank=True,null=True,default=staff_shift_code)
    name = models.CharField(max_length=50,verbose_name='Shift Name')
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_buf_min = models.IntegerField(default=0)
    end_buf_min = models.IntegerField(default=0)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True,null=True)
    remarks = models.CharField(max_length=255,blank=True,null=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='staff_shift_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='staff_shift_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sta_shift'
        
    def __str__(self):
        return str(self.name)

class Staff(models.Model):
    code = models.CharField(max_length=20, blank=True, null=True,verbose_name='Staff Code')
    staff_id = models.CharField(max_length=20, blank=True,null=True,editable=False, verbose_name='Staff ID',default=staff_no)
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='First Name')
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Last Name')
    gender = models.ForeignKey(Gender,on_delete=models.SET_NULL,blank=True,null=True,related_name='staff_gender')
    dob = models.DateField(null=True, blank=True, verbose_name='Date of Birth')
    photo = models.ImageField(upload_to='staff_photo/',blank=True, null=True, verbose_name='Photo')
    mobile_no = models.CharField(max_length=14,blank=True,null=True,verbose_name='Mobile No')
    emergency_number = models.CharField(max_length=14,blank=True,null=True,verbose_name='Emergency Contact Number')
    nid = models.CharField(max_length=17,blank=True,null=True,verbose_name='NID')
    religion = models.ForeignKey(Religion,on_delete=models.SET_NULL,blank=True,null=True,related_name='staff_gender')
    email = models.EmailField(max_length=255,blank=True,null=True, verbose_name='Email Address')
    blood_group = models.ForeignKey(BloodGroup,on_delete=models.SET_NULL,blank=True,null=True,related_name='staff_b_group')
    marital_status = models.ForeignKey(MaritalStatus,on_delete=models.SET_NULL,blank=True,null=True,related_name='staff_marital_status')
    present_address = models.TextField(verbose_name='Present Address', blank=True,null=True)
    permanent_address = models.TextField(verbose_name='Permanent Address', blank=True,null=True)
    doj = models.DateField(blank=True,null=True,verbose_name='Date Of Join')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, blank=True, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
    shift = models.ForeignKey(StaffShift, on_delete=models.SET_NULL, blank=True, null=True)
    step = models.IntegerField(default=1)
    user = models.OneToOneField(Authentication,on_delete=models.SET_NULL, blank=True,null=True)
    category = models.ForeignKey(ContractType, on_delete=models.SET_NULL, blank=True, null=True)
    staff_status = models.ForeignKey(ActiveStatus, on_delete=models.SET_NULL, blank=True, null=True)
    last_attn_proc_date = models.DateField(blank=True,null=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='staff_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='staff_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sta_staff'

    def __str__(self):
        return self.first_name
    
    def name(self):
        return f'{self.first_name} {self.last_name}'
    
class Education(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True,null=True,related_name='staff_education')
    order_seq = models.IntegerField(blank=True,null=True)
    institution_name = models.CharField(max_length=255, blank=True, null=True)
    registration_no = models.CharField(max_length=50, blank=True,null=True)
    title = models.CharField(max_length=255,blank=True,null=True)
    edu_board = models.ForeignKey(EducationBoard,on_delete=models.SET_NULL, blank=True,null=True, verbose_name='Board')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True,null=True)
    passing_year = models.IntegerField(blank=True, null=True)
    result = models.CharField(max_length=20, blank=True,null=True)
    result_out_of = models.CharField(max_length=50, blank=True,null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='education_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='education_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sta_education'

    def __str__(self):
        return str(self.title)

class StaffPayroll(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True,null=True,related_name='payroll')
    order_seq = models.IntegerField(default=0)
    gross = models.IntegerField()
    basic = models.IntegerField(default=0)
    medical = models.IntegerField(default=0)
    convence = models.IntegerField(default=0)
    others = models.IntegerField(default=0)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    salary_Setup = models.ForeignKey(SalarySetupMst,on_delete=models.SET_NULL,blank=True,null=True)
    remarks = models.CharField(max_length=255,blank=True, null=True)
    contract_type = models.ForeignKey(ContractType, on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='payroll_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='payroll_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sta_payroll'

    def __str__(self):
        return str(self.gross)
    
class StaffBankAccountDetails(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True,null=True,related_name='bank_info')
    account_title = models.CharField(max_length=255,verbose_name='Account Title')
    account_number = models.CharField(max_length=50, verbose_name='Account Number')
    bank_name = models.ForeignKey(AccountBank,on_delete=models.CASCADE)
    branch_name = models.CharField(max_length=100, verbose_name='Branch Name')
    remarks = models.CharField(max_length=255,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='bank_acc_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='bank_acc_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sta_bank_account'

    def __str__(self):
        return str(self.account_title)

class StaffSocialMedia(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True,null=True,related_name='social_media')
    name = models.CharField(max_length=50, verbose_name='Media Name')
    username = models.CharField(max_length=50, verbose_name='Username/ID')
    url = models.URLField(max_length=255,verbose_name='URL')
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='socal_media_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='socal_media_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sta_social_media'

    def __str__(self):
        return str(self.name)
    
class StaffLeave(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True,null=True,related_name='staff_leave')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.SET_NULL, blank=True, null=True,related_name='staff_leave_type')
    leave_days = models.IntegerField(default=0)
    process_days = models.IntegerField(default=0)
    taken_days = models.IntegerField(default=0)
    start_date = models.DateField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='staff_leave_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='staff_leave_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sta_leave'

    def __str__(self):
        return str(self.id)
    
    def clean(self):
        super().clean()
        # Check if leave_days is greater than the max_days for the associated LeaveType
        if self.leave_type and self.leave_days > self.leave_type.max_days and self.leave_type.is_active and self.leave_type.status:
            raise ValidationError({'leave_days': f"Leave days cannot be greater than {self.leave_type.name}'s max_days ({self.leave_type.max_days})."})
        # Ensure that taken_days is not greater than leave_days
        if self.taken_days > self.leave_days:
            raise ValidationError({'taken_days': 'Taken days cannot be greater than leave days'})

class ProcessAttendanceDaily(models.Model):
    attn_date = models.DateField(verbose_name='Attendance Date',blank=True,null=True)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True,null=True, related_name='atten_daily')
    shift = models.ForeignKey(StaffShift, on_delete=models.SET_NULL, blank=True, null=True)
    staff_code = models.CharField(max_length=20, blank=True,null=True)
    con_type = models.ForeignKey(ContractType, on_delete=models.SET_NULL, blank=True,null=True,verbose_name='Contract Type')
    attn_type = models.ForeignKey(AttendanceType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Attendance Type')
    process_date = models.DateTimeField(blank=True,null=True)
    in_time = models.DateTimeField(blank=True,null=True)
    out_time = models.DateTimeField(blank=True,null=True)
    duration = models.DurationField(blank=True,null=True, verbose_name='Duraion')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, blank=True, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
    late_by_min = models.DurationField(blank=True,null=True)
    early_gone_by_min = models.DurationField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='atten_daily_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='atten_daily_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'proc_attn_daily'

    def __str__(self):
        return str(self.id)
    
    def get_day_name(self):
        return self.attn_date.strftime('%A')
    
    
@receiver(pre_save, sender=ProcessAttendanceDaily)        
def calculate_duration(sender, instance, **kwargs):
    if instance.in_time and instance.out_time:
        duration = instance.out_time - instance.in_time
        instance.duration = duration
    else:
        instance.duration = None

@receiver(pre_save, sender=ProcessAttendanceDaily)  
def cal_late_min(sender,instance,**kwargs):
    from datetime import datetime
    if instance.in_time and instance.in_time.time() > instance.shift.start_time:
        in_time = instance.in_time.time()
        shift_start_time = instance.shift.start_time
        in_time = datetime.combine(datetime.today(), in_time)
        shift_start_time = datetime.combine(datetime.today(), shift_start_time)
        late_by_min = in_time - shift_start_time
        instance.late_by_min = late_by_min
    else:
        instance.late_by_min = None

    if instance.out_time and instance.in_time and instance.in_time != instance.out_time and instance.shift.end_time > instance.out_time.time():
        out_time = instance.out_time.time()
        shift_end_time = instance.shift.end_time
        out_time = datetime.combine(datetime.today(), out_time)
        shift_end_time = datetime.combine(datetime.today(), shift_end_time)
        early_gone_by_min = shift_end_time - out_time
        instance.early_gone_by_min = early_gone_by_min
    else:
        instance.early_gone_by_min = None
    


class AttendanceDailyRaw(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True,null=True, related_name='raw_atten')
    staff_code = models.CharField(max_length=20, blank=True,null=True)
    attn_date = models.DateField(verbose_name='Attendance Date',blank=True,null=True)
    trnsc_time = models.DateTimeField(blank=True, null=True)
    device_ip = models.GenericIPAddressField(blank=True,null=True)
    device_name = models.CharField(max_length=255,blank=True,null=True)
    device_serial = models.CharField(max_length=255, blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    mobile = models.CharField(max_length=255,blank=True,null=True)
    username = models.CharField(max_length=255,blank=True,null=True)
    src_type = models.CharField(max_length=20,blank=True,null=True)
    attn_type = models.CharField(max_length=20,blank=True,null=True)
    remarks = models.CharField(max_length=500, blank=True,null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='atten_raw_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='atten_raw_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'raw_attn_daily'

    def __str__(self):
        return str(self.id)

def leave_code():
    last_leave_code = StaffLeaveTransaction.objects.all().order_by('code').last()
    if not last_leave_code or last_leave_code.code is None:
        return 'LV-' + '01'
    leave_num = str(last_leave_code.code)[-2:]
    leave_num_int = int(leave_num)
    new_leave_num = leave_num_int + 1
    new_gd_num = 'LV-' + str(new_leave_num).zfill(2)
    return new_gd_num   
  
class StaffLeaveTransaction(models.Model):
    code = models.CharField(max_length=20,editable=False, verbose_name='Leave Code',default=leave_code)
    start_date = models.DateField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.SET_NULL, blank=True, null=True)
    tran_type = models.CharField(max_length=20, blank=True, null=True)
    day_count = models.IntegerField(blank=True, null=True, editable=False, verbose_name='Number of Day')
    application_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    add_during_leave = models.TextField(blank=True, null=True)
    reason_for_leave = models.TextField(blank=True,null=True)
    apply_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True,related_name='staff_leave_trns')
    responsible = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True,related_name='resonsible_by')
    document = models.FileField(upload_to='staff_leave_doc/', blank=True, null=True, verbose_name='Document',validators=[validate_pdf_file_size])
    remarks = models.TextField(blank=True, null=True)
    app_status = models.ForeignKey(Setup, on_delete=models.SET_NULL,blank=True, null=True,limit_choices_to={'parent__type': 'APPROVAL_STATUS'},related_name='approval_status')
    active_start_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    active_end_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='staff_trns_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='staff_trns_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.end_date and self.start_date:
            if self.end_date < self.start_date:
                raise ValidationError('End date must be greater than or equal to start date.')
        # print(self.apply_by.id,self.leave_type)
        # print(self.day_count)
        try:
            leave_status = StaffLeave.objects.get(staff=self.apply_by,leave_type=self.leave_type,is_active=True,status=True)
            remain_days = (leave_status.leave_days-leave_status.taken_days)
            print(self.day_count)
            if leave_status.leave_days <= leave_status.taken_days:
                # raise ValidationError(f'Sorry!! You have already taken all {self.leave_type}')
                raise ValidationError(f'দুঃখিত!! আপনি ইতিমধ্যে সব {self.leave_type} গ্রহণ করেছেন')
            if remain_days <= self.day_count:
                raise ValidationError(f'You can not apply {self.day_count} days because your remaining {self.leave_type} has {remain_days} days !!!')
                # raise ValidationError(f'আপনি {self.day_count} দিন {self.leave_type} ছুটি আবেদন করতে পারবেন না কারণ আপনার ছুটি বাকি আছে {remain_days} দিন !!!')
        except StaffLeave.DoesNotExist:
            raise ValidationError(f'Sorry!! You have not assign {self.leave_type}')
            
        # if self.leave_type and self.day_count > self.leave_type. and self.leave_type.is_active and self.leave_type.status:

    # def save(self, *args, **kwargs):
    #     self.clean()
    #     super().save(*args, **kwargs)

    class Meta:
        db_table = 'staff_leave_trns'

    def __str__(self):
        return str(self.code)

@receiver(pre_save, sender=StaffLeaveTransaction)
def calculate_duration(sender, instance, **kwargs):
    if instance.start_date and instance.end_date:
        duration = 1 + (instance.end_date - instance.start_date).days
        instance.day_count = duration
    else:
        instance.day_count = None

@receiver(post_save, sender=StaffLeaveTransaction)
def status_update_in_attn(sender, instance, **kwargs):
    if instance.app_status.type == 'APPROVED':
        attn_type_id = AttendanceType.objects.filter(status=True,name__iexact=instance.leave_type.leave_type_code).last()
        if attn_type_id:
            ProcessAttendanceDaily.objects.filter(status=True,is_active=True,staff=instance.apply_by,attn_date__range=(instance.start_date, instance.end_date)).update(attn_type=attn_type_id)
        else:
            print('Something worng in attendance type data')

@receiver(post_save, sender=StaffLeaveTransaction)
def delete_leave(sender, instance, **kwargs):
    if instance.status==False:
        instance.day_count
        leave_bal = StaffLeave.objects.filter(staff=instance.apply_by,leave_type=instance.leave_type,status=True,is_active=True,institution=instance.institution,branch=instance.branch).last()
        StaffLeave.objects.filter(pk=leave_bal.pk).update(process_days=leave_bal.process_days - instance.day_count)

# @receiver(post_save, sender=StaffLeaveTransaction)
# def update_taken_day(sender,instance,**kwargs):
#     total_taken_days = StaffLeaveTransaction.objects.get(
#                                         apply_by=instance.apply_by,
#                                         leave_type=instance.leave_type,
#                                         status=True,
#                                         is_active=True
#                                     ).values('apply_by', 'leave_type').annotate(
#                                         total_days=Sum('day_count')
#                                     ).values('total_days')
#     print(total_taken_days['total_days'])
#     leave_status = StaffLeave.objects.get(staff=instance.apply_by,leave_type=instance.leave_type,is_active=True,status=True)
#     print(leave_status.taken_days)

class StaffLeaveAppHistory(models.Model):
    leave_trns = models.ForeignKey(StaffLeaveTransaction, on_delete=models.SET_NULL,blank=True,null=True,related_name='approval_path')
    approve_group = models.ForeignKey(Setup, on_delete=models.SET_NULL,blank=True,null=True,limit_choices_to={'parent__type': 'STAFF_LEAVE_APP_HIR'},related_name='app_group')
    approve_by = models.ForeignKey(Staff, on_delete=models.SET_NULL,blank=True,null=True)
    app_status = models.ForeignKey(Setup, on_delete=models.SET_NULL,blank=True, null=True,limit_choices_to={'parent__type': 'APPROVAL_STATUS'},related_name='app_status')
    remarks = models.TextField(blank=True,null=True)
    approve_date = models.DateTimeField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='staff_trns_his_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='staff_trns_his_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'staff_leave_approve_history'

    def __str__(self):
        return str(self.id)

@receiver(post_save, sender=StaffLeaveAppHistory)
def update_leave_approval_status(sender, instance, **kwargs):
    if instance.app_status:
        from datetime import datetime
        print(instance.leave_trns.day_count,instance.leave_trns.leave_type,instance.leave_trns.apply_by)
        leave_bal = StaffLeave.objects.filter(staff=instance.leave_trns.apply_by,leave_type=instance.leave_trns.leave_type,status=True,is_active=True,institution=instance.institution,branch=instance.branch).last()
        print('******',leave_bal.leave_days,leave_bal.process_days)
        try:
            if instance.app_status.type == 'APPROVED':
                StaffLeave.objects.filter(pk=leave_bal.pk).update(
                    process_days=leave_bal.process_days - instance.leave_trns.day_count,
                    taken_days=leave_bal.taken_days + instance.leave_trns.day_count
                )
            elif instance.app_status.type == 'DENY':
                StaffLeave.objects.filter(pk=leave_bal.pk).update(
                    process_days=leave_bal.process_days - instance.leave_trns.day_count
                )
            else:
                pass
        except Exception as e:
            print(f"Error updating StaffLeave: {e}")
        instance.leave_trns.app_status = instance.app_status
        instance.leave_trns.save()


def staff_atnn_code():
    last_staff_attn_code = ProcessStaffAttendanceMst.objects.all().order_by('id').last()
    if not last_staff_attn_code or last_staff_attn_code.code is None:
        return 'P-' + '1'
    staff_attn_mst_num = str(last_staff_attn_code.code)[2:]
    staff_attn_mst_num_int = int(staff_attn_mst_num)
    new_staff_attn_mst_num = staff_attn_mst_num_int + 1
    new_gd_num = 'P-' + str(new_staff_attn_mst_num)
    return new_gd_num   

class ProcessStaffAttendanceMst(models.Model):
    code = models.CharField(max_length=15,verbose_name='Code',default=staff_atnn_code,editable=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    staff_code = models.CharField(max_length=100, blank=True,null=True)
    from_date = models.DateField()
    to_date = models.DateField()
    staff_payroll = models.ForeignKey(StaffPayroll, on_delete=models.SET_NULL, blank=True, null=True)
    total_day = models.IntegerField(default=0,editable=False)
    present_day = models.IntegerField(default=0)
    absent_day = models.IntegerField(default=0)
    late_day = models.IntegerField(default=0)
    early_gone_day = models.IntegerField(default=0)
    tot_payble_day = models.IntegerField(default=0)
    ot_hour = models.IntegerField(default=0)
    gen_type = models.CharField(max_length=15, default='AUTO')
    tour_day = models.IntegerField(default=0)
    weekend_day = models.IntegerField(default=0)
    holiday_day = models.IntegerField(default=0)
    actual_gross = models.IntegerField(default=0)
    calc_gross = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='staff_proc_atnn_mst_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='staff_proc_atnn_mst_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'staff_proc_out_attn_mst'

    def save(self, *args, **kwargs):
        # Calculate the number of days between from_date and to_date
        if self.from_date and self.to_date:
            delta = self.to_date - self.from_date
            self.total_day = delta.days + 1
        else:
            self.total_day = 0
        
        # Call the original save method
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.code)

def staff_status_code():
    last_staff_status_code = StaffStatusTransaction.objects.all().order_by('code').last()
    if not last_staff_status_code or last_staff_status_code.code is None:
        return 'M-' + '1'
    staff_status_num = str(last_staff_status_code.code)[2:]
    staff_status_num_int = int(staff_status_num)
    new_staff_status_num = staff_status_num_int + 1
    new_gd_num = 'M-' + str(new_staff_status_num)
    return new_gd_num  

class StaffStatusTransaction(models.Model):
    code = models.CharField(max_length=15,default=staff_status_code,editable=False)
    start_date = models.DateTimeField(blank=True,null=True)
    end_date = models.DateTimeField(blank=True,null=True)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL,blank=True,null=True)
    staff_status = models.ForeignKey(ActiveStatus, on_delete=models.SET_NULL, blank=True, null=True)
    reason = models.TextField()
    remarks = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='staff_status_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='staff_status_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'staff_status_trns'

    def __str__(self):
        return str(self.code)
    
@receiver(post_save, sender=StaffStatusTransaction)
def update_staff_status(sender, instance, **kwargs):
    if instance.staff:
        instance.staff.staff_status = instance.staff_status
        instance.staff.save()

class ProcessStaffSalaryTable(models.Model):
    staff=models.ForeignKey(Staff, on_delete=models.SET_NULL,blank=True,null=True)
    staff_no = models.CharField(max_length=50,blank=True,null=True)
    staff_name = models.CharField(max_length=200,blank=True,null=True)
    staff_payroll = models.ForeignKey(StaffPayroll, on_delete=models.SET_NULL,blank=True,null=True)
    department = models.ForeignKey(Department,on_delete=models.SET_NULL,blank=True,null=True)
    designation = models.ForeignKey(Designation,on_delete=models.SET_NULL, blank=True,null=True)
    from_date = models.DateField()
    to_date = models.DateField()
    bank_acc_no = models.CharField(max_length=255,blank=True,null=True)
    is_hold = models.BooleanField(default=False)
    prl_ele_basic = models.IntegerField(blank=True,null=True)
    prl_ele_house_rent = models.IntegerField(blank=True,null=True)
    prl_ele_medical = models.IntegerField(blank=True,null=True)
    prl_ele_conveyance = models.IntegerField(blank=True,null=True)
    prl_ele_others_a = models.IntegerField(blank=True,null=True)
    gross = models.IntegerField(blank=True,null=True)
    prl_ele_adjustment_a = models.IntegerField(blank=True,null=True)
    prl_ele_adjustment_d = models.IntegerField(blank=True,null=True)
    prl_ele_cash_advance = models.IntegerField(blank=True,null=True)
    prl_ele_donation = models.IntegerField(blank=True,null=True)
    prl_ele_award = models.IntegerField(blank=True,null=True)
    prl_ele_ait = models.IntegerField(blank=True,null=True)
    prl_ele_mobile_bill_d = models.IntegerField(blank=True,null=True)
    prl_ele_rpf = models.IntegerField(blank=True,null=True)
    prl_ele_other_d = models.IntegerField(blank=True,null=True)
    prl_ele_absent_d = models.IntegerField(blank=True,null=True)
    prl_ele_food_d = models.IntegerField(blank=True,null=True)
    total_deduction = models.IntegerField(blank=True,null=True)
    new_payable_amt = models.IntegerField(blank=True,null=True)
    payable_day = models.IntegerField(blank=True,null=True)
    remarks = models.TextField(blank=True,null=True)
    is_paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='proc_sal_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='proc_sal_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'staff_proc_sal_tbl'

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        if self.from_date > self.to_date:
            raise ValidationError(_("The 'from_date' cannot be greater than the 'to_date'."))
        if self.id is None:
            data_count = ProcessStaffSalaryTable.objects.filter(Q(status=True),Q(is_active=True),Q(staff=self.staff),
                                                                Q(from_date__range=(self.from_date, self.to_date)) | Q(to_date__range=(self.from_date, self.to_date))
                                                                ).count()
            if data_count > 0:
                raise ValidationError(_("The data already exists."))
        super(ProcessStaffSalaryTable, self).save(*args, **kwargs)


@receiver(pre_save, sender=ProcessStaffSalaryTable)
def fill_staff_info(sender, instance, **kwargs):
    if instance.staff:
        instance.staff_no = instance.staff.staff_id
        instance.staff_name = instance.staff.first_name+' '+instance.staff.last_name
        instance.department = instance.staff.department
        instance.designation = instance.staff.designation
        payroll_info=StaffPayroll.objects.filter(status=True,is_active=True,staff=instance.staff,
                                                        institution=instance.institution,branch=instance.branch).last()
        if payroll_info:
            instance.staff_payroll = payroll_info
            if payroll_info.salary_Setup:
                context = {
                        'gross_pay': payroll_info.gross,
                    }
                for sal_dtl_ele in SalarySetupDtl.objects.filter(status=True, salary_setup_mst=payroll_info.salary_Setup).order_by('seq_order'):
                    import ast
                    
                    if sal_dtl_ele.payroll_ele.name == 'Gross Salary':
                        formatted_formula = sal_dtl_ele.formula.format(**context)
                        gross_pay = eval(compile(ast.parse(formatted_formula, mode='eval'), '', 'eval'))
                        instance.gross = gross_pay
                        instance.new_payable_amt = gross_pay
                        context['gross_pay'] = gross_pay  # Update context with the calculated gross pay
                    elif sal_dtl_ele.payroll_ele.name == 'Basic Pay':
                        formatted_formula = sal_dtl_ele.formula.format(**context)
                        basic_pay = eval(compile(ast.parse(formatted_formula, mode='eval'), '', 'eval'))
                        instance.prl_ele_basic = basic_pay
                        context['basic_pay'] = basic_pay  # Update context with the calculated basic pay
                    elif sal_dtl_ele.payroll_ele.name == 'House Rent':
                        context.update({
                            'basic_pay':basic_pay,  # Ensure basic_pay is added to the context
                        })
                        formatted_formula = sal_dtl_ele.formula.format(**context)
                        house_rent = eval(compile(ast.parse(formatted_formula, mode='eval'), '', 'eval'))
                        if sal_dtl_ele.max_amt and house_rent > sal_dtl_ele.max_amt:
                            house_rent = sal_dtl_ele.max_amt
                        instance.prl_ele_house_rent = house_rent
                        context['house_rent'] = house_rent  # Update context with the calculated house rent

                    elif sal_dtl_ele.payroll_ele.name == 'Medical':
                        context.update({
                            'house_rent': house_rent,  # Ensure house_rent is added to the context
                        })
                        
                        formatted_formula = sal_dtl_ele.formula.format(**context)
                        medical_pay = eval(compile(ast.parse(formatted_formula, mode='eval'), '', 'eval'))
                        if sal_dtl_ele.max_amt and medical_pay > sal_dtl_ele.max_amt:
                            medical_pay = sal_dtl_ele.max_amt
                        instance.prl_ele_medical = medical_pay
                        context['medical'] = medical_pay  # Update context with the calculated medical pay
                        
                    elif sal_dtl_ele.payroll_ele.name == 'Conveyance':
                        context.update({
                            'medical': medical_pay,  # Ensure medical is added to the context
                        })
                        formatted_formula = sal_dtl_ele.formula.format(**context)
                        conveyance_pay = eval(compile(ast.parse(formatted_formula, mode='eval'), '', 'eval'))
                        if sal_dtl_ele.max_amt and conveyance_pay > sal_dtl_ele.max_amt:
                            conveyance_pay = sal_dtl_ele.max_amt
                        instance.prl_ele_conveyance = conveyance_pay
                        context['convence'] = conveyance_pay  # Update context with the calculated conveyance pay

                    elif sal_dtl_ele.payroll_ele.name == 'Other':
                        context.update({
                            'convence': conveyance_pay,  # Ensure conveyance is added to the context
                        })
                        formatted_formula = sal_dtl_ele.formula.format(**context)
                        others_pay = eval(compile(ast.parse(formatted_formula, mode='eval'), '', 'eval'))
                        instance.prl_ele_others_a = others_pay
            else:
                instance.gross = None
                instance.prl_ele_basic = None
                instance.prl_ele_house_rent = None
                instance.prl_ele_medical = None
                instance.prl_ele_conveyance = None
                instance.prl_ele_others_a = None



        account_info = StaffBankAccountDetails.objects.filter(status=True,is_active=True,staff=instance.staff,
                                                        institution=instance.institution,branch=instance.branch).last()
        if account_info:
            instance.bank_acc_no = account_info.account_number

        if instance.from_date and instance.to_date:
            duration = 1 + (instance.to_date - instance.from_date).days
            instance.payable_day = duration
        else:
            instance.payable_day = None
            
@receiver(post_save, sender=ProcessStaffSalaryTable)
def account_posting(sender, instance, **kwargs):
    if instance.is_paid:
        print(instance.new_payable_amt)
        # For Debit amt
        acc_coa = ChartofAccounts.objects.filter(status=True,coa_type='EXPENSE',title__iexact='salary',institution=instance.institution,branch=instance.branch).last()
        acc_coa_ref = ChartofAccounts.objects.filter(status=True,coa_type='ASSET',title__iexact='cash',institution=instance.institution,branch=instance.branch).last()
        print(acc_coa.code,acc_coa_ref.code)
        acc_dbt_ledger = {}
        from datetime import datetime
        acc_dbt_ledger['gl_date'] = datetime.now().strftime('%Y-%m-%d')
        acc_dbt_ledger['acc_coa'] = acc_coa
        acc_dbt_ledger['acc_coa_ref'] = acc_coa_ref
        print(acc_dbt_ledger)

        print('okay...................')
    
