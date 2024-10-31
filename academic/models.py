from django.db import models
from institution.models import Institution, Branch
from django_userforeignkey.models.fields import UserForeignKey
import uuid
from django.contrib.auth.models import User
from setup_app.models import Days, FloorType, SubjectType
from staff.models import Staff
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from staff.models import Staff
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db.models import UniqueConstraint
from django.db import models, IntegrityError

def generate_unique_code():
    return str(uuid.uuid4().hex[:10])  # Adjust the length as needed

def validate_alpha_chars_only(value):
    if not value.replace(' ', '').isalpha():
        raise ValidationError(
            _('The field can only contain alphabetic characters.'),
            code='alpha_chars_only'
        )
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

class ClassGroup(models.Model):
    code = models.CharField(max_length=20,blank=True,null=True,verbose_name='Code')
    name = models.CharField(max_length=50,verbose_name='Group Name',validators=[validate_alpha_chars_only])
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='class_group_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='class_group_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ac_group'
        verbose_name = 'Class Group'
    
    def __str__(self):
        return str(self.name)

class Subject(models.Model):
    code = models.CharField(max_length=20, blank=True,null=True,verbose_name='Subject Code')
    type = models.ForeignKey(SubjectType,on_delete=models.SET_NULL,blank=True, null=True,verbose_name='Subject Type')
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
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True)
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
    floor_type = models.ForeignKey(FloorType, on_delete=models.SET_NULL,blank=True, null=True)
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
    duration = models.DurationField(blank=True,null=True, verbose_name='Class Duraion', editable=False)
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

@receiver(pre_save, sender=ClassPeriod)        
def calculate_duration(sender, instance, **kwargs):
    if instance.start_time and instance.end_time:
        # Get the current date for the calculation
        current_date = datetime.now().date()

        # Convert start_time and end_time to datetime objects
        start_datetime = datetime.combine(current_date, instance.start_time)
        end_datetime = datetime.combine(current_date, instance.end_time)

        # Ensure both start_time and end_time are on the same date
        if start_datetime > end_datetime:
            # In case end_time is on the next day, adjust it
            end_datetime += timedelta(days=1)

        duration = end_datetime - start_datetime
        instance.duration = duration
    else:
        instance.duration = None


class ClassSection(models.Model):
    class_name = models.ForeignKey(ClassName, on_delete=models.SET_NULL, blank=True, null=True)
    section = models.ForeignKey(Section,on_delete=models.SET_NULL,blank=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, blank=True, null=True)
    version = models.ForeignKey(Version, on_delete=models.SET_NULL, blank=True, null=True)
    group = models.ForeignKey(ClassGroup, on_delete=models.SET_NULL,blank=True,null=True)
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
        return str(self.id)

def validate_pdf_extension(value):
    if not value.name.lower().endswith('.pdf'):
        raise ValidationError('Only PDF files are allowed.')

def validate_pdf_file_size(value):
    if value.size > 20 * 1024 * 1024:  # 20MB in bytes
        raise ValidationError('File size cannot exceed 20MB.')

# class PDFFileField(models.FileField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('validators', []).append(FileExtensionValidator(allowed_extensions=['pdf']))
#         super().__init__(*args, **kwargs)

class PDFFileField(models.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('validators', []).extend([
            FileExtensionValidator(allowed_extensions=['pdf']),
        ])
        super().__init__(*args, **kwargs)

class ClassSubject(models.Model):
    class_name = models.ForeignKey(ClassName, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Class Name')
    section = models.ForeignKey(Section,on_delete=models.SET_NULL,blank=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, blank=True, null=True)
    version = models.ForeignKey(Version, on_delete=models.SET_NULL, blank=True, null=True)
    group = models.ForeignKey(ClassGroup, on_delete=models.SET_NULL, blank=True,null=True)
    code = models.CharField(max_length=20, blank=True, null=True, verbose_name='Subject Code')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to='book_images/', blank=True, null=True, verbose_name='Book Image')
    book_file = PDFFileField(upload_to='book_file/', blank=True, null=True, verbose_name='Book File',validators=[validate_pdf_file_size])
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
        return str(self.code) + ' | ' +str(self.subject.name) + ' | ' + str(self.subject.type)

class ClassTeacher(models.Model):
    version = models.ForeignKey(Version, on_delete=models.CASCADE, verbose_name='Version')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name='Session')
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE, verbose_name='Class Name')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Section')
    group = models.ForeignKey(ClassGroup, on_delete=models.SET_NULL,blank=True,null=True)
    teacher = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name='Teacher Name')
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,blank=True,null=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='class_teacher_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='class_teacher_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ac_class_teacher'
        verbose_name = 'Assign Class Teacher'
        constraints = [
            UniqueConstraint(fields=['session','teacher','status','institution','branch'], name='unique_teacher_constraint')
        ] 
    
    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            raise ValidationError({"message": "This teacher already assign for this session"})

class ClassRoutine(models.Model):
    teacher = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name='Teacher Name')
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE, verbose_name='Class Name')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Section')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name='Session')
    version = models.ForeignKey(Version, on_delete=models.CASCADE, verbose_name='Version')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Subject')
    class_period = models.ForeignKey(ClassPeriod, on_delete=models.CASCADE, verbose_name='Class Period')
    day = models.ForeignKey(Days,on_delete=models.CASCADE, verbose_name='Day')
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

class ClassRoutineMst(models.Model):
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE, verbose_name='Class Name')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Section')
    group = models.ForeignKey(ClassGroup, on_delete=models.SET_NULL,blank=True,null=True, verbose_name='Group')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name='Session')
    version = models.ForeignKey(Version, on_delete=models.CASCADE, verbose_name='Version')
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,blank=True,null=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='class_routine_mst_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='class_routine_mst_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ac_class_routine_mst'
        verbose_name = 'Class Routine'
    
    def __str__(self):
        return str(self.id)
    
class ClassRoutiineDtl(models.Model):
    class_routine_mst = models.ForeignKey(ClassRoutineMst, on_delete=models.CASCADE, related_name='routine_dtl')
    day = models.ForeignKey(Days,on_delete=models.CASCADE, verbose_name='Day')
    teacher = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name='Teacher Name')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL,blank=True,null=True, verbose_name='Subject')
    class_subject = models.ForeignKey(ClassSubject,on_delete=models.SET_NULL, verbose_name='Class Subject',blank=True,null=True)
    class_period = models.ForeignKey(ClassPeriod, on_delete=models.CASCADE, verbose_name='Class Period')
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE,blank=True, null=True, verbose_name='Class Room')
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,blank=True,null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='class_routine_dtl_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='class_routine_dtl_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ac_class_routine_dtl'
    
    def __str__(self):
        return str(self.id)


