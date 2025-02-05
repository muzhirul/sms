from django.db import models
from academic.models import ClassName, Section, Session, Version, ClassGroup
from institution.models import Institution, Branch
from staff.models import StaffShift,Staff
from django_userforeignkey.models.fields import UserForeignKey
from authentication.models import Authentication
import datetime
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from setup_app.models import *
from django.core.validators import RegexValidator
from django.db.models import UniqueConstraint
# For generate student number
def generate_student_no():
    last_stuent_no = Student.objects.all().order_by('student_no').last()
    if not last_stuent_no or last_stuent_no.student_no is None:
        return '77'+str(datetime.date.today().year) + str(datetime.date.today().month).zfill(2) + '00'
    student_num = str(last_stuent_no.student_no)[-2:]
    student_num_int = int(student_num)
    new_student_num = student_num_int + 1
    new_std_num = '77'+str(str(datetime.date.today().year)) + str(datetime.date.today().month).zfill(2) + str(new_student_num).zfill(2)
    return new_std_num
# Create your models here.

def validate_pdf_file_size(value):
    if value.size > 2 * 1024 * 1024:  # 20MB in bytes
        raise ValidationError('File size cannot exceed 2MB.')

class Category(models.Model):
    name = models.CharField(max_length=50,verbose_name='Category Name')
    sl_no = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL, related_name='st_category_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='st_category_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'st_category'

    def __str__(self):
        return str(self.name)

class Student(models.Model):
    code = models.CharField(max_length=10,blank=True,null=True)
    student_no = models.CharField(max_length=15,blank=True,null=True,editable=False, verbose_name='Student No', default=generate_student_no)
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='First Name')
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Last Name')
    gender = models.ForeignKey(Gender,on_delete=models.SET_NULL,blank=True,null=True,related_name='student_gender')
    dob = models.DateField(null=True, blank=True, verbose_name='Date of Birth')
    photo = models.ImageField(upload_to='student_photo/',blank=True, null=True, verbose_name='Photo')
    mobile_no = models.CharField(max_length=14,blank=True,null=True,verbose_name='Mobile No', validators=[
        RegexValidator(
            # regex=r'^(?:\+88|01)[3-9]\d{8}$',
            # regex=r'^\+880[1-9][0-9]{8}$|^01[3-9][0-9]{8}$',
            regex = r'^(?:\+8801[3-9][0-9]{8}|01[3-9][0-9]{8})$',
            message="Invalid Bangladeshi mobile number format.",
            code='invalid_mobile_number'
        )
    ],help_text="Enter a valid Bangladeshi mobile number (e.g., +8801712XXXXXX or 01712XXXXXX).")
    religion = models.ForeignKey(Religion,on_delete=models.SET_NULL,blank=True,null=True,related_name='student_religion')
    email = models.EmailField(max_length=255,blank=True,null=True, verbose_name='Email Address')
    admission_date = models.DateField(blank=True, null=True,verbose_name='Admission Date')
    birth_reg_scert_no = models.CharField(max_length=20,blank=True,null=True, verbose_name='Birth Registration Certificate No')
    birth_cert_file = models.FileField(upload_to='birth_regi/', blank=True, null=True, verbose_name='জন্ম নিবন্ধন সনদ',validators=[validate_pdf_file_size])
    blood_group = models.ForeignKey(BloodGroup,on_delete=models.SET_NULL,blank=True,null=True,related_name='student_b_group')
    present_address = models.TextField(verbose_name='Present Address', blank=True,null=True)
    permanent_address = models.TextField(verbose_name='Permanent Address', blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,blank=True,null=True)
    shift = models.ForeignKey(StaffShift, on_delete=models.SET_NULL, blank=True, null=True)
    std_status = models.ForeignKey(ActiveStatus, on_delete=models.SET_NULL, blank=True, null=True)
    step = models.IntegerField(default=1)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True)
    user = models.OneToOneField(Authentication,on_delete=models.SET_NULL, blank=True,null=True)
    is_online = models.BooleanField(default=False, verbose_name='Is Online')
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='student_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='student_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'st_student'

    def __str__(self):
        return self.first_name
 
# For generate student number
def generate_guardian_no():
    last_guardian_no = Guardian.objects.all().order_by('guardian_no').last()
    if not last_guardian_no or last_guardian_no.guardian_no is None:
        return '11'+str(datetime.date.today().year) + str(datetime.date.today().month).zfill(2) + '00'
    guardian_num = str(last_guardian_no.guardian_no)[-2:]
    guardian_num_int = int(guardian_num)
    new_guardian_num = guardian_num_int + 1
    new_gd_num = '11'+str(str(datetime.date.today().year)) + str(datetime.date.today().month).zfill(2) + str(new_guardian_num).zfill(2)
    return new_gd_num   

class Guardian(models.Model):
    guardian_no = models.CharField(max_length=15,blank=True,null=True,editable=False, verbose_name='Guardian No', default=generate_guardian_no)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name="guardians")
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='First Name')
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Last Name')
    gender = models.ForeignKey(Gender,on_delete=models.SET_NULL,blank=True,null=True,related_name='guardian_gender')
    relation = models.ForeignKey(Relation,on_delete=models.SET_NULL,blank=True,null=True,related_name='guardian_relation')
    occupation = models.ForeignKey(Occupation,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='guardian_occupation')
    nid = models.CharField(max_length=20, null=True,blank=True, verbose_name='NID')
    photo = models.ImageField(upload_to='guardian_photo/',blank=True,null=True)
    mobile_no = models.CharField(max_length=14,blank=True,null=True,verbose_name='Mobile No', validators=[
        RegexValidator(
            # regex=r'^(?:\+88|01)[3-9]\d{8}$',
            # regex=r'^\+880[1-9][0-9]{8}$|^01[3-9][0-9]{8}$',
            regex = r'^(?:\+8801[3-9][0-9]{8}|01[3-9][0-9]{8})$',
            message="Invalid Bangladeshi mobile number format.",
            code='invalid_mobile_number'
        )
    ],help_text="Enter a valid Bangladeshi mobile number (e.g., +8801712XXXXXX or 01712XXXXXX).")
    is_guardian = models.BooleanField(default=False)
    user = models.OneToOneField(Authentication,on_delete=models.SET_NULL, blank=True,null=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='st_guardian_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='st_guardian_updated_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'st_guardian'

    def __str__(self):
        return self.first_name
    

@receiver(post_save, sender=Guardian)
def create_user_from_guardian(sender, instance, **kwargs):
    """
    Signal to create a user for a Guardian if certain conditions are met.
    """
    if not instance.is_guardian or instance.user:
        return  # Exit if not a guardian or user already exists

    # Check if an active user is already linked to the student's guardians
    if Guardian.objects.filter(student=instance.student, user__isnull=False, status=True).exists():
        print(f'Guardian user already exists for this student {instance.studen}.')
        return

    ga_user_type = 'GUARDIAN'
    default_password = '12345678'

    def create_authentication_user(username):
        """Helper function to create an Authentication user."""
        ga_user = Authentication(
            username=username,
            first_name=instance.first_name,
            model_name='Guardian',
            last_name=instance.last_name,
            user_type=ga_user_type,
            is_active=True,
            institution=instance.student.institution,
            branch=instance.student.branch
        )
        ga_user.set_password(default_password)
        ga_user.save()
        return ga_user

    # Check if the username exists, else create a new one
    if not Authentication.objects.filter(username=instance.guardian_no).exists():
        ga_user = create_authentication_user(instance.guardian_no)
    else:
        last_user = Authentication.objects.filter(username__startswith='11').order_by('-username').first()
        new_username = str(int(last_user.username) + 1) if last_user else '11000001'
        ga_user = create_authentication_user(new_username)
        instance.guardian_no = new_username

    # Link the created user to the Guardian instance
    instance.user = ga_user
    instance.save()
    
# @receiver(post_save, sender=Guardian)
# def create_user_from_guardian(sender, instance, **kwargs):
#     """
#     Signal to automatically create a user for a Guardian if they meet specific conditions.
#     """
#     if instance.is_guardian and not instance.user:
#         # Check if any active user is already linked to the student's guardians
#         active_user_count = Guardian.objects.filter(
#             student=instance.student, 
#             user__isnull=False, 
#             status=True
#         ).count()

#         if active_user_count == 0:
#             ga_user_type = 'GUARDIAN'
#             default_password = '12345678'

#             # Check if the username already exists
#             if not Authentication.objects.filter(username=instance.guardian_no).exists():
#                 # Create a new user
#                 ga_user = Authentication(
#                     username=instance.guardian_no,
#                     first_name=instance.first_name,
#                     model_name='Guardian',
#                     last_name=instance.last_name,
#                     user_type=ga_user_type,
#                     is_active=True,
#                     institution=instance.student.institution,
#                     branch=instance.student.branch
#                 )
#                 ga_user.set_password(default_password)
#                 ga_user.save()

#                 # Link the created user to the Guardian instance
#                 instance.user = ga_user
#                 instance.save()
#             else:
#                 # Generate a new username if it already exists
#                 last_user = Authentication.objects.filter(username__startswith='11').order_by('username').last()
#                 if last_user:
#                     new_username = str(int(last_user.username) + 1)
#                 # Create a new user with the new username
#                 ga_user = Authentication(
#                     username=new_username,
#                     first_name=instance.first_name,
#                     model_name='Guardian',
#                     last_name=instance.last_name,
#                     user_type=ga_user_type,
#                     is_active=True,
#                     institution=instance.student.institution,
#                     branch=instance.student.branch
#                 )
#                 ga_user.set_password(default_password)
#                 ga_user.save()

#                 # Update the Guardian instance with the new user and guardian number
#                 instance.user = ga_user
#                 instance.guardian_no = new_username
#                 instance.save()
#         else:
#             print('Guardian user already exists.')

# @receiver(post_save, sender=Guardian)
# def create_user_from_guardian(sender, instance, **kwargs):
#     if instance.is_guardian and not instance.user:
#         aaa = Guardian.objects.filter(student=instance.student,user__isnull=False,status=True).count()
#         if aaa == 0:
#             ga_user_type = 'GUARDIAN'
#             default_password = '12345678'
#             if not Authentication.objects.filter(username=instance.guardian_no).exists():
                
#                 ga_user = Authentication(username=instance.guardian_no,first_name=instance.first_name,model_name='Guardian',
#                                          last_name=instance.last_name,user_type=ga_user_type,is_active=True,
#                                          institution=instance.student.institution, branch=instance.student.branch)
#                 ga_user.set_password(default_password)
#                 ga_user.save()
#                 instance.user = ga_user
#                 instance.save()
#             else:
#                 last_ga_username = Authentication.objects.filter(username__startswith='11').order_by('username').last()
#                 int_last_ga_username = int(last_ga_username.username)
#                 new_ga_username = (int_last_ga_username+1)
#                 print(new_ga_username)
#                 ga_user = Authentication(username=new_ga_username,first_name=instance.first_name,model_name='Guardian',
#                                          last_name=instance.last_name,user_type=ga_user_type,is_active=True,
#                                          institution=instance.student.institution, branch=instance.student.branch)
#                 ga_user.set_password(default_password)
#                 ga_user.save()
#                 instance.user = ga_user
#                 instance.guardian_no = new_ga_username
#                 instance.save()
#         else:
#             print('Already exists....')



class StudentEnroll(models.Model):
    version = models.ForeignKey(Version, on_delete=models.CASCADE, verbose_name='version')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name='Session')
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE, verbose_name='Class Name')
    shift = models.ForeignKey(StaffShift, on_delete=models.SET_NULL, blank=True, null=True)
    group = models.ForeignKey(ClassGroup,on_delete=models.SET_NULL, blank=True,null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Section')
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, verbose_name='Student',related_name="enroll",blank=True,null=True)
    roll = models.IntegerField(verbose_name='Class Roll',blank=True,null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    remarks = models.CharField(max_length=255,blank=True, null=True)
    admission_paid = models.CharField(max_length=10,default='Unpaid')
    is_active = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='student_enroll_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='student_enroll_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'st_enroll'
        constraints = [
            UniqueConstraint(fields=['student','version','session','class_name','status','institution','branch'], name='unique_std_enroll_constraint'),
            UniqueConstraint(fields=['version','session','class_name','shift','group','section','roll','status','institution','branch'], name='unique_std_enroll_roll_const')
        ] 
        
    def __str__(self):
        return str(self.roll)
    
    def save(self, *args, **kwargs):
        if not self.roll:
            last_roll = StudentEnroll.objects.filter(version=self.version,session=self.session,
                                                     class_name=self.class_name,shift=self.shift,
                                                     group=self.group,section=self.section,status=True,is_active=True,
                                                     institution=self.institution,branch=self.branch).order_by('-roll').first()
            if last_roll and last_roll.roll is not None:
                self.roll = (last_roll.roll + 1)
            else:
                self.roll = 1
        super().save(*args, **kwargs)


@receiver(post_save, sender=StudentEnroll)
def update_std_shift(sender, instance, **kwargs):
    if instance.student:
        last_enroll = StudentEnroll.objects.filter(status=True,is_active=True,institution=instance.institution,branch=instance.branch).last()
        instance.student.shift = last_enroll.shift
        instance.student.save()

@receiver(post_save, sender=StudentEnroll)
def insert_fees_trns(sender, instance, **kwargs):
    from fees.models import FeesMaster,FeesDetails, FeesTransaction
    fees_mst = FeesMaster.objects.filter(status=True,version=instance.version,session=instance.session,
                                         class_name=instance.class_name,group=instance.group,section=instance.section,
                                         institution=instance.institution,branch=instance.branch).order_by('id').last()
    fees_dtl = FeesDetails.objects.filter(status=True,is_active=True,institution=instance.institution,branch=instance.branch,fees_master=fees_mst,
                                          fees_type__category='admission').order_by('id').last()
    FeesTransaction.objects.filter(status=True, is_active=True,institution=instance.institution,
                                   branch=instance.branch,pay_status=False).exclude(fees_detail=fees_dtl).update(status=False)
    if fees_dtl:
        trns_count = FeesTransaction.objects.filter(status=True,student=instance.student,fees_detail=fees_dtl,institution=instance.institution,branch=instance.branch).count()
        if trns_count == 0:
            std_fees_trns = {}
            std_fees_trns['student'] = instance.student
            std_fees_trns['fees_detail'] = fees_dtl
            std_fees_trns['institution'] = instance.institution
            std_fees_trns['branch'] = instance.branch
            t = FeesTransaction.objects.create(**std_fees_trns)
    

class ProcessStAttendanceDaily(models.Model):
    attn_date = models.DateField(verbose_name='Attendance Date',blank=True,null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL,blank=True,null=True, related_name='std_atten_daily')
    shift = models.ForeignKey(StaffShift, on_delete=models.SET_NULL, blank=True, null=True)
    student_code = models.CharField(max_length=20, blank=True,null=True)
    version = models.ForeignKey(Version, on_delete=models.CASCADE, verbose_name='version', blank=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name='Session', blank=True, null=True)
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE, verbose_name='Class Name', blank=True, null=True)
    group = models.ForeignKey(ClassGroup,on_delete=models.SET_NULL, blank=True,null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Section', blank=True, null=True)
    roll = models.CharField(max_length=15,verbose_name='Class Roll',blank=True,null=True)
    attn_type = models.ForeignKey(AttendanceType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Attendance Type')
    process_date = models.DateTimeField(blank=True,null=True)
    in_time = models.DateTimeField(blank=True,null=True)
    out_time = models.DateTimeField(blank=True,null=True)
    duration = models.DurationField(blank=True,null=True, verbose_name='Duraion')
    late_by_min = models.DurationField(blank=True,null=True)
    early_gone_by_min = models.DurationField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='st_atten_daily_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='st_atten_daily_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'st_attn_daily'

    def __str__(self):
        return str(self.attn_date)
    
    def get_day_name(self):
        return self.attn_date.strftime('%A')
    
@receiver(pre_save, sender=ProcessStAttendanceDaily)        
def calculate_duration(sender, instance, **kwargs):
    if instance.in_time and instance.out_time:
       
        duration = instance.out_time - instance.in_time
        instance.duration = duration
    else:
        instance.duration = None

@receiver(pre_save, sender=ProcessStAttendanceDaily)  
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

def leave_code():
    last_leave_code = StudentLeaveTransaction.objects.all().order_by('code').last()
    if not last_leave_code or last_leave_code.code is None:
        return 'SLV-' + '01'
    leave_num = str(last_leave_code.code)[-2:]
    leave_num_int = int(leave_num)
    new_leave_num = leave_num_int + 1
    new_gd_num = 'SLV-' + str(new_leave_num).zfill(2)
    return new_gd_num  

class StudentLeaveTransaction(models.Model):
    code = models.CharField(max_length=20,editable=False, verbose_name='Leave Code',default=leave_code)
    start_date = models.DateField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True)
    tran_type = models.CharField(max_length=20, blank=True, null=True)
    day_count = models.IntegerField(blank=True, null=True, editable=False, verbose_name='Number of Day')
    application_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    add_during_leave = models.TextField(blank=True, null=True)
    reason_for_leave = models.TextField(blank=True,null=True)
    apply_by = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True,related_name='std_leave_trns')
    shift = models.ForeignKey(StaffShift, on_delete=models.SET_NULL, blank=True, null=True)
    student_code = models.CharField(max_length=20, blank=True,null=True)
    version = models.ForeignKey(Version, on_delete=models.CASCADE, verbose_name='version', blank=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name='Session', blank=True, null=True)
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE, verbose_name='Class Name', blank=True, null=True)
    group = models.ForeignKey(ClassGroup,on_delete=models.SET_NULL, blank=True,null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Section', blank=True, null=True)
    roll = models.CharField(max_length=15,verbose_name='Class Roll',blank=True,null=True)
    document = models.FileField(upload_to='std_leave_doc/', blank=True, null=True, verbose_name='Document',validators=[validate_pdf_file_size])
    responsible = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True,related_name='std_leave_responsible')
    remarks = models.TextField(blank=True, null=True)
    app_status = models.ForeignKey(Setup, on_delete=models.SET_NULL,blank=True, null=True,limit_choices_to={'parent__type': 'APPROVAL_STATUS'},related_name='std_approval_status')
    active_start_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    active_end_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='std_trns_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='std_trns_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.end_date and self.start_date:
            if self.end_date < self.start_date:
                raise ValidationError('End date must be greater than or equal to start date.')

    class Meta:
        db_table='std_leave_trns'

    def __str__(self):
        return str(self.code)

@receiver(pre_save, sender=StudentLeaveTransaction)
def calculate_duration(sender, instance, **kwargs):
    if instance.start_date and instance.end_date:
        duration = 1 + (instance.end_date - instance.start_date).days
        instance.day_count = duration
    else:
        instance.day_count = None

def staff_status_code():
    last_staff_status_code = StudentStatusTransaction.objects.all().order_by('code').last()
    if not last_staff_status_code or last_staff_status_code.code is None:
        return 'STS-' + '1'
    staff_status_num = str(last_staff_status_code.code)[4:]
    staff_status_num_int = int(staff_status_num)
    new_staff_status_num = staff_status_num_int + 1
    new_gd_num = 'STS-' + str(new_staff_status_num)
    return new_gd_num  

class StudentStatusTransaction(models.Model):
    code = models.CharField(max_length=15,default=staff_status_code,editable=False)
    start_date = models.DateTimeField(blank=True,null=True)
    end_date = models.DateTimeField(blank=True,null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL,blank=True,null=True)
    std_status = models.ForeignKey(ActiveStatus, on_delete=models.SET_NULL, blank=True, null=True)
    reason = models.TextField()
    remarks = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='std_status_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='std_status_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'std_status_trns'

    def __str__(self):
        return str(self.code)

@receiver(post_save, sender=Student)
def insert_std_status(sender, instance, created, **kwargs):
    if created:
        active_status = ActiveStatus.objects.filter(status=True, is_active=True,name__iexact='active').last()
        StudentStatusTransaction.objects.create(
            student = instance,
            start_date = instance.admission_date,
            reason="New student registration",
            std_status=active_status,
            institution = instance.institution,
            branch = instance.branch
        )

@receiver(post_save, sender=StudentStatusTransaction)
def update_staff_status(sender, instance, **kwargs):
    if instance.student:
        instance.student.std_status = instance.std_status
        instance.student.save()

class PreviousEducation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='pre_education')
    name = models.CharField(max_length=255,verbose_name='Previous Institution Name')
    address = models.TextField()
    class_name = models.CharField(max_length=255)
    roll_no = models.IntegerField()
    document = models.FileField(upload_to='pre_edu_doc/',blank=True, null=True, verbose_name='Document')
    reason = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='pre_edu_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='pre_edu_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'std_previous_edu'

    def __str__(self):
        return str(self.name)
    
