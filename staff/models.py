from django.db import models
from institution.models import Institution, Branch
from django_userforeignkey.models.fields import UserForeignKey
# Create your models here.
class staff(models.Model):
    GENDER_TYPE = (('M','Male'),('F','Female'),('O','Other'))
    RELIGION_TYPE = (('M','Muslim'),('H','Hindu'))
    BLOOD_GROUP_TYPE = (('A+','A+'),('A-','A-'))
    code = models.CharField(max_length=20, blank=True, null=True, verbose_name='Staff Code')
    staff_id = models.CharField(max_length=20, blank=True,null=True, verbose_name='Staff ID')
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='First Name')
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Last Name')
    gender = models.CharField(max_length=10, blank=True, null=True, choices=GENDER_TYPE)
    dob = models.DateField(null=True, blank=True, verbose_name='Date of Birth')
    photo = models.ImageField(upload_to='staff_photo/',blank=True, null=True, verbose_name='Photo')
    mobile_no = models.CharField(max_length=11,blank=True,null=True,verbose_name='Mobile No')
    religion = models.CharField(max_length=10, blank=True, null=True, choices=RELIGION_TYPE)
    email = models.EmailField(max_length=255,blank=True,null=True, verbose_name='Email Address')
    blood_group = models.CharField(max_length=5, blank=True,null=True,choices=BLOOD_GROUP_TYPE, verbose_name='Blood Group')
    present_address = models.TextField(verbose_name='Present Address', blank=True,null=True)
    permanent_address = models.TextField(verbose_name='Permanent Address', blank=True,null=True)
    Institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
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
    
class Education(models.Model):
    staff = models.ForeignKey(staff, on_delete=models.SET_NULL, blank=True,null=True)
    order_seq = models.IntegerField(blank=True,null=True)
    institution_name = models.CharField(max_length=255, blank=True, null=True)
    registration_no = models.CharField(max_length=50, blank=True,null=True)
    title = models.CharField(max_length=255,blank=True,null=True)
    board = models.CharField(max_length=50, blank=True,null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True,null=True)
    passing_year = models.IntegerField(blank=True, null=True)
    result = models.CharField(max_length=20, blank=True,null=True)
    result_out_of = models.CharField(max_length=50, blank=True,null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    Institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='education_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='education_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sta_education'

    def __str__(self):
        return self.title
    
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
        return self.name
    

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
        return self.name
