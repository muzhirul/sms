from django.db import models
from institution.models import Institution
from django_userforeignkey.models.fields import UserForeignKey

# Create your models here.
class Version(models.Model):
    code = models.CharField(max_length=20, blank=True,null=True,verbose_name='Version Code')
    version = models.IntegerField(blank=True,null=True, verbose_name='Version')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True,null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='version_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='version_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ac_version'
        verbose_name = '1. Versions'

    def __str__(self):
        return self.version
    
class Session(models.Model):
    code = models.CharField(max_length=20,blank=True,null=True,verbose_name='Session Code')
    session = models.IntegerField(blank=True,null=True,verbose_name='Session')
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='session_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='session_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ac_session'
        verbose_name = '2. Section'
    
    def __str__(self):
        return self.session

class Section(models.Model):
    code = models.CharField(max_length=20,blank=True,null=True,verbose_name='Section Code')
    section = models.IntegerField(blank=True,null=True,verbose_name='Section')
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='section_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='section_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ac_section'
        verbose_name = '3. Section'
    
    def __str__(self):
        return self.section
    

class Subject(models.Model):
    code = models.CharField(max_length=20, blank=True,null=True,verbose_name='Subject Code')
    type = models.CharField(max_length=20, blank=True, null=True,verbose_name='Subject Type')
    name = models.CharField(max_length=100, blank=True,null=True,verbose_name='Subject Name')
    picture = models.ImageField(upload_to='subject_img/',blank=True,null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True,null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='subject_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='subject_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ac_subject'
        verbose_name = '4. Subject'

class Class(models.Model):
    code = models.CharField(max_length=10,blank=True,null=True,verbose_name='Class Code')
    name = models.CharField(max_length=50,blank=True,null=True, verbose_name='Class Name')
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True)
    section = models.ManyToManyField(Section)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='class_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='class_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ac_class'
        verbose_name = '5. Class'

    def __str__(self):
        return self.name
