from django.db import models
from django.core.exceptions import ValidationError
from institution.models import Institution, Branch
from setup_app.models import Role
from django_userforeignkey.models.fields import UserForeignKey

# Create your models here.
def validate_file_size(value):
    if value.size > 5 * 1024 * 1024:  # 20MB in bytes
        raise ValidationError('File size cannot exceed 5MB.')
    
class NoticeBoard(models.Model):
    title = models.CharField(max_length=100)
    notice_date = models.DateField()
    publish_date = models.DateField()
    attachment = models.FileField(upload_to='notice_board/',validators=[validate_file_size])
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