from django.db import models
from institution.models import Institution, Branch
from django_userforeignkey.models.fields import UserForeignKey
import uuid
from django.contrib.auth.models import User
from setup_app.models import Day, FloorType
from staff.models import Staff

def generate_unique_code():
    return str(uuid.uuid4().hex[:10])  # Adjust the length as needed



# Create your models here.
class Version(models.Model):
    code = models.CharField(max_length=20, blank=True,null=True,verbose_name='Version Code', unique=True, default=generate_unique_code)
    version = models.CharField(max_length=20,blank=True,null=True, verbose_name='Version')
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True,null=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='version_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='version_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ac_version'
        verbose_name = '1. Version'

    def __str__(self):
        return self.version
    
class Session(models.Model):
    code = models.CharField(max_length=20,blank=True,null=True,verbose_name='Session Code', unique=True, default=generate_unique_code)
    session = models.CharField(max_length=100,blank=True,null=True,verbose_name='Session')
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='session_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='session_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ac_session'
        verbose_name = '2. Session'
    
    def __str__(self):
        return str(self.session)

class Section(models.Model):
    code = models.CharField(max_length=20,blank=True,null=True,verbose_name='Section Code', unique=True, default=generate_unique_code)
    section = models.CharField(max_length=50,blank=True,null=True,verbose_name='Section')
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='section_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='section_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ac_section'
        verbose_name = '3. Section'
    
    def __str__(self):
        return str(self.section)
    

class Subject(models.Model):
    SUBJECT_TYPE = (('THEORY','Theory'),('PARCTICAL','Practical'))
    code = models.CharField(max_length=20, blank=True,null=True,verbose_name='Subject Code')
    type = models.CharField(max_length=20, blank=True, null=True,verbose_name='Subject Type',choices=SUBJECT_TYPE)
    name = models.CharField(max_length=100, blank=True,null=True,verbose_name='Subject Name')
    picture = models.ImageField(upload_to='subject_img/',blank=True,null=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True,null=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='subject_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='subject_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ac_subject'
        verbose_name = '4. Subject'

    def __str__(self):
        return str(self.code) + ' | ' +str(self.name) + ' | ' + str(self.type)

class ClassName(models.Model):
    code = models.CharField(max_length=10,blank=True,null=True,verbose_name='Class Code')
    name = models.CharField(max_length=50,blank=True,null=True, verbose_name='Class Name')
    # section = models.ForeignKey(Section,on_delete=models.SET_NULL,blank=True,null=True)
    # version = models.ForeignKey(Version, on_delete=models.SET_NULL,blank=True,null=True)
    # session = models.ForeignKey(Session, on_delete=models.SET_NULL,blank=True,null=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True)
    # section = models.ManyToManyField(Section)
    # subject = models.ManyToManyField(Subject)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='class_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='class_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ac_class'
        verbose_name = '5. Class'

    def __str__(self):
        return str(self.name)
    
class ClassRoom(models.Model):
    code = models.CharField(max_length=20, blank=True,null=True,verbose_name='Room Code')
    floor_type = models.ForeignKey(FloorType, on_delete=models.SET_NULL,blank=True, null=True, related_name="floor")
    building = models.CharField(max_length=100, blank=True,null=True, verbose_name='Building Name')
    room_no = models.CharField(max_length=10, blank=True, null=True, verbose_name='Room No.')
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True,null=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='class_room_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='class_room_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ac_class_room'
        verbose_name = '6. Class Room'

    def __str__(self):
        return self.room_no
    
class ClassPeriod(models.Model):
    code = models.CharField(max_length=10, blank=True,null=True, verbose_name='Class Period Code')
    name = models.CharField(max_length=100, blank=True,null=True,verbose_name='Class Period Name')
    start_time = models.TimeField(blank=True,null=True)
    end_time = models.TimeField(blank=True,null=True)
    duration = models.IntegerField(blank=True,null=True,verbose_name='Class Duration')
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True,null=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='class_period_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='class_period_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ac_class_period'
        verbose_name = '7. Class Period'

    def __str__(self):
        return self.name

class ClassSection(models.Model):
    class_name = models.ForeignKey(ClassName, on_delete=models.SET_NULL, blank=True, null=True)
    section = models.ForeignKey(Section,on_delete=models.SET_NULL,blank=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, blank=True, null=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='class_section_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='class_section_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ac_class_section'
        verbose_name = '8. Class section'

    def __str__(self):
        return str(self.class_name.name) +' | '+str(self.section.section)

class ClassSubject(models.Model):
    class_name = models.ForeignKey(ClassName, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Class Name')
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, blank=True,null=True)
    code = models.CharField(max_length=20, blank=True, null=True, verbose_name='Subject Code')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to='book_images/', blank=True, null=True, verbose_name='Book Image')
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='class_subject_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='class_subject_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ac_class_subject'
        verbose_name = '9. Class Subject'

    def __str__(self):
        return str(self.class_name.name)
    
class ClassRoutine(models.Model):
    DAY_TYPE = (('SUNDAY','SUNDAY'),('MONDAY','MONDAY'),('TUESDAY','TUESDAY'),('WEDNESDAY','WEDNESDAY'),('THURSDAY','THURSDAY'))
    teacher = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name='Teacher Name')
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE, verbose_name='Class Name')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Section')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name='Session')
    version = models.ForeignKey(Version, on_delete=models.CASCADE, verbose_name='Version')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Subject')
    class_period = models.ForeignKey(ClassPeriod, on_delete=models.CASCADE, verbose_name='Class Period')
    day = models.ForeignKey(Day,on_delete=models.CASCADE, verbose_name='Day')
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE,blank=True, null=True, verbose_name='Class Room')
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,blank=True,null=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='class_routine_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='class_routine_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ac_class_routine'
        verbose_name = 'Class Routine'
    
    def __str__(self):
        return self.day.short_name