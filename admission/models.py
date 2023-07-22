from django.db import models

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
    mobile_no = models.CharField(max_length=11,blank=True,null=True,verbose_name='Mobile No')
    religion = models.CharField(max_length=10, blank=True, null=True, choices=RELIGION_TYPE)
    email = models.EmailField(max_length=255,blank=True,null=True, verbose_name='Email Address')
    admission_date = models.DateField(blank=True, null=True,verbose_name='Admission Date')
    blood_group = models.CharField(max_length=5, blank=True,null=True,choices=BLOOD_GROUP_TYPE, verbose_name='Blood Group')
    present_address = models.TextField(verbose_name='Present Address', blank=True,null=True)
    permanent_address = models.TextField(verbose_name='Permanent Address', blank=True,null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admission'

    def __str__(self):
        return self.first_name