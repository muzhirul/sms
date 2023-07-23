from django.db import models
from institution.models import Institution
from django_userforeignkey.models.fields import UserForeignKey

# Create your models here.
class Admission(models.Model):
    GENDER_TYPE = (('M','Male'),('F','Female'),('O','Other'))
    RELIGION_TYPE = (('M','Muslim'),('H','Hindu'))
    BLOOD_GROUP_TYPE = (('A+','A+'),('A-','A-'))
    code = models.CharField(max_length=10,blank=True,null=True)
    admission_no = models.CharField(max_length=15,blank=True,null=True,editable=False, verbose_name='Admission No')
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='First Name')
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Last Name')
    gender = models.CharField(max_length=10, blank=True, null=True, choices=GENDER_TYPE)
    dob = models.DateField(null=True, blank=True, verbose_name='Date of Birth')
    photo = models.ImageField(upload_to='admission_photo/',blank=True, null=True, verbose_name='Photo')
    mobile_no = models.CharField(max_length=11,blank=True,null=True,verbose_name='Mobile No')
    religion = models.CharField(max_length=10, blank=True, null=True, choices=RELIGION_TYPE)
    email = models.EmailField(max_length=255,blank=True,null=True, verbose_name='Email Address')
    admission_date = models.DateField(blank=True, null=True,verbose_name='Admission Date')
    blood_group = models.CharField(max_length=5, blank=True,null=True,choices=BLOOD_GROUP_TYPE, verbose_name='Blood Group')
    present_address = models.TextField(verbose_name='Present Address', blank=True,null=True)
    permanent_address = models.TextField(verbose_name='Permanent Address', blank=True,null=True)
    Institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    is_online = models.BooleanField(default=False, verbose_name='Is Online')
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='admission_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='admission_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admission'

    def __str__(self):
        return self.first_name
    
class Guardian(models.Model):
    GENDER_TYPE = (('M','Male'),('F','Female'),('O','Other'))
    RELIGION_TYPE = (('M','Muslim'),('H','Hindu'))
    BLOOD_GROUP_TYPE = (('A+','A+'),('A-','A-'))
    OCUPATION_TYPE = (('DOCTOR','Doctor'),('TEACHER','Teacher'),('OTHER','Other'))
    RELATION_TYPE = (('FATHER','Father'),('MOTHER','Mother'),('BROTHER','Brother'),('SISTER','Sister'))
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE,related_name="admission_guardian")
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='First Name')
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Last Name')
    gender = models.CharField(max_length=10, blank=True, null=True, choices=GENDER_TYPE)
    relation = models.CharField(max_length=20,blank=True,null=True,choices=RELATION_TYPE)
    ocupation = models.CharField(max_length=10,blank=True,null=True,choices=OCUPATION_TYPE,verbose_name='Ocupation')
    nid = models.CharField(max_length=20, null=True,blank=True, verbose_name='NID')
    photo = models.ImageField(upload_to='guardian_photo/',blank=True,null=True)
    mobile_no = models.CharField(max_length=11,blank=True,null=True,verbose_name='Mobile No')
    is_guardian = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='guardian_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='guardian_updated_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ad_guardian'

    def __str__(self):
        return self.first_name