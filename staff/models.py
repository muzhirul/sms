from django.db import models
from institution.models import Institution, Branch
from setup_app.models import EducationBoard
from django_userforeignkey.models.fields import UserForeignKey
from setup_app.models import *
from hrms.models import AccountBank, LeaveType
import datetime
from authentication.models import Authentication
# Create your models here.

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
        return str(self.id)
    
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






    
