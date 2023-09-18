from django.db import models
from institution.models import Institution, Branch
from django_userforeignkey.models.fields import UserForeignKey
from authentication.models import Authentication
import datetime
# For generate student number
def generate_student_no():
    last_stuent_no = Student.objects.all().order_by('student_no').last()
    if not last_stuent_no or last_stuent_no.student_no is None:
        return 'ST-'+str(datetime.date.today().year) + str(datetime.date.today().month).zfill(2) + '00'
    student_num = str(last_stuent_no.student_no)[-2:]
    student_num_int = int(student_num)
    new_student_num = student_num_int + 1
    new_std_num = 'ST-'+str(str(datetime.date.today().year)) + str(datetime.date.today().month).zfill(2) + str(new_student_num).zfill(2)
    return new_std_num
# Create your models here.
class Student(models.Model):
    GENDER_TYPE = (('M','Male'),('F','Female'),('O','Other'))
    RELIGION_TYPE = (('M','Muslim'),('H','Hindu'))
    BLOOD_GROUP_TYPE = (('A+','A+'),('A-','A-'))
    code = models.CharField(max_length=10,blank=True,null=True)
    student_no = models.CharField(max_length=15,blank=True,null=True,editable=False, verbose_name='Student No', default=generate_student_no)
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='First Name')
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Last Name')
    gender = models.CharField(max_length=10, blank=True, null=True, choices=GENDER_TYPE)
    dob = models.DateField(null=True, blank=True, verbose_name='Date of Birth')
    photo = models.ImageField(upload_to='student_photo/',blank=True, null=True, verbose_name='Photo')
    mobile_no = models.CharField(max_length=11,blank=True,null=True,verbose_name='Mobile No')
    religion = models.CharField(max_length=10, blank=True, null=True, choices=RELIGION_TYPE)
    email = models.EmailField(max_length=255,blank=True,null=True, verbose_name='Email Address')
    admission_date = models.DateField(blank=True, null=True,verbose_name='Admission Date')
    blood_group = models.CharField(max_length=5, blank=True,null=True,choices=BLOOD_GROUP_TYPE, verbose_name='Blood Group')
    present_address = models.TextField(verbose_name='Present Address', blank=True,null=True)
    permanent_address = models.TextField(verbose_name='Permanent Address', blank=True,null=True)
    Institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
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
        return 'G-'+str(datetime.date.today().year) + str(datetime.date.today().month).zfill(2) + '00'
    guardian_num = str(last_guardian_no.guardian_no)[-2:]
    guardian_num_int = int(guardian_num)
    new_guardian_num = guardian_num_int + 1
    new_gd_num = 'G-'+str(str(datetime.date.today().year)) + str(datetime.date.today().month).zfill(2) + str(new_guardian_num).zfill(2)
    return new_gd_num   
class Guardian(models.Model):
    GENDER_TYPE = (('M','Male'),('F','Female'),('O','Other'))
    RELIGION_TYPE = (('M','Muslim'),('H','Hindu'))
    BLOOD_GROUP_TYPE = (('A+','A+'),('A-','A-'))
    OCUPATION_TYPE = (('DOCTOR','Doctor'),('TEACHER','Teacher'),('OTHER','Other'))
    RELATION_TYPE = (('FATHER','Father'),('MOTHER','Mother'),('BROTHER','Brother'),('SISTER','Sister'))
    guardian_no = models.CharField(max_length=15,blank=True,null=True,editable=False, verbose_name='Guardian No', default=generate_guardian_no)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name="guardians")
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='First Name')
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Last Name')
    gender = models.CharField(max_length=10, blank=True, null=True, choices=GENDER_TYPE)
    relation = models.CharField(max_length=20,blank=True,null=True,choices=RELATION_TYPE)
    ocupation = models.CharField(max_length=10,blank=True,null=True,choices=OCUPATION_TYPE,verbose_name='Ocupation')
    nid = models.CharField(max_length=20, null=True,blank=True, verbose_name='NID')
    photo = models.ImageField(upload_to='guardian_photo/',blank=True,null=True)
    mobile_no = models.CharField(max_length=11,blank=True,null=True,verbose_name='Mobile No')
    is_guardian = models.BooleanField(default=False)
    user = models.OneToOneField(Authentication,on_delete=models.SET_NULL, blank=True,null=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='st_guardian_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='st_guardian_updated_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'st_guardian'

    def __str__(self):
        return self.first_name
