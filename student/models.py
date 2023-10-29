from django.db import models
from institution.models import Institution, Branch
from django_userforeignkey.models.fields import UserForeignKey
from authentication.models import Authentication
import datetime
from setup_app.models import *
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
class Student(models.Model):
    GENDER_TYPE = (('M','Male'),('F','Female'),('O','Other'))
    RELIGION_TYPE = (('M','Muslim'),('H','Hindu'))
    BLOOD_GROUP_TYPE = (('A+','A+'),('A-','A-'))
    code = models.CharField(max_length=10,blank=True,null=True)
    student_no = models.CharField(max_length=15,blank=True,null=True,editable=False, verbose_name='Student No', default=generate_student_no)
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='First Name')
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Last Name')
    gender = models.ForeignKey(Gender,on_delete=models.SET_NULL,blank=True,null=True,related_name='student_gender')
    dob = models.DateField(null=True, blank=True, verbose_name='Date of Birth')
    photo = models.ImageField(upload_to='student_photo/',blank=True, null=True, verbose_name='Photo')
    mobile_no = models.CharField(max_length=11,blank=True,null=True,verbose_name='Mobile No')
    religion = models.ForeignKey(Religion,on_delete=models.SET_NULL,blank=True,null=True,related_name='student_religion')
    email = models.EmailField(max_length=255,blank=True,null=True, verbose_name='Email Address')
    admission_date = models.DateField(blank=True, null=True,verbose_name='Admission Date')
    blood_group = models.ForeignKey(BloodGroup,on_delete=models.SET_NULL,blank=True,null=True,related_name='student_b_group')
    present_address = models.TextField(verbose_name='Present Address', blank=True,null=True)
    permanent_address = models.TextField(verbose_name='Permanent Address', blank=True,null=True)
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
