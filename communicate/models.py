from django.db import models
from django.core.exceptions import ValidationError
from institution.models import Institution, Branch
from setup_app.models import Role
from academic.models import ClassSection,Section
from staff.models import Staff
from student.models import Student, Guardian
from bleach import clean
from academic.models import ClassSection
from django_userforeignkey.models.fields import UserForeignKey

# Create your models here.
def validate_file_size(value):
    if value.size > 5 * 1024 * 1024:  # 20MB in bytes
        raise ValidationError('File size cannot exceed 5MB.')
    
class NoticeBoard(models.Model):
    title = models.CharField(max_length=100)
    notice_date = models.DateField()
    publish_date = models.DateField()
    attachment = models.FileField(upload_to='notice_board/',blank=True,null=True,validators=[validate_file_size])
    description = models.TextField()
    notice_for = models.ManyToManyField(Role)
    status = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='notice_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='notice_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comm_notice_board'
        verbose_name = 'Notice Board'

    def __str__(self):
        return str(self.title)
    
class SmsTemplate(models.Model):
    title = models.CharField(max_length=255)
    message_body = models.TextField()
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='sms_temp_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='sms_temp_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comm_sms_template'
        verbose_name = 'SMS Template'

    def __str__(self):
        return str(self.title)
    
class SmsEmailLog(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    email_recipient_list = models.TextField(default='')
    email_cc_recipient_list = models.TextField(default='')
    cc_staff = models.ManyToManyField(Staff, blank=True, related_name='sms_email_log_cc_staff')
    cc_students = models.ManyToManyField(Student, blank=True, related_name='sms_email_log_cc_students')
    cc_guardians = models.ManyToManyField(Guardian, blank=True, related_name='sms_email_log_cc_guardians')
    sms_recipient_list = models.TextField(default='')
    is_active = models.BooleanField(default=True)
    email = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    sms = models.BooleanField(default=False)
    sms_sent = models.BooleanField(default=False)
    mobile_app = models.BooleanField(default=False, blank=True, null=True)
    group = models.BooleanField(default=False)
    group_ids = models.ManyToManyField(Role, blank=True)
    individual = models.BooleanField(default=False)
    individual_staff = models.ManyToManyField(Staff, blank=True, related_name='sms_email_log_individual_staff')
    individual_students = models.ManyToManyField(Student, blank=True, related_name='sms_email_log_individual_students')
    individual_guardians = models.ManyToManyField(Guardian, blank=True, related_name='sms_email_log_individual_guardians')
    academic_class = models.BooleanField(default=False)
    academic_class_info = models.ForeignKey(ClassSection, on_delete=models.SET_NULL, blank=True, null=True, related_name='sms_email_log_academic_class_info')
    academic_class_sections_info = models.ManyToManyField(Section, blank=True, related_name='sms_email_log_academic_class_sections_info')
    birthdays = models.BooleanField(default=False)
    birthdays_staff = models.ManyToManyField(Staff, blank=True, related_name='sms_email_log_birthdays_staff')
    birthdays_students = models.ManyToManyField(Student, blank=True, related_name='sms_email_log_birthdays_students')
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='sms_email_log_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='sms_email_log_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comm_sms_email_log'
        verbose_name = 'SMS Email Log'

    def __str__(self):
        return str(self.subject)
    
    def clean(self):
        if self.message:  
            self.message = clean(self.message, tags=None, attributes=None, strip=False)
        else:
            self.message = ""

class SmsEmailLogAttachment(models.Model):
    sms_email_log = models.ForeignKey(SmsEmailLog, on_delete=models.CASCADE, related_name='attachments')
    attachment = models.ImageField(upload_to='sms_email_log_attachments/', blank=True, null=True, verbose_name='Attachment')

    class Meta:
        db_table = 'comm_sms_email_log_attachments'
        verbose_name = 'SMS Email Log Attachment'

    def __str__(self):
        return f"Attachment for {self.sms_email_log.subject}"    

    


    