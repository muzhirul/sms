from django.db import models
from django_userforeignkey.models.fields import UserForeignKey
from institution.models import Institution, Branch
from setup_app.models  import HolidayType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
def validate_alpha_chars_only(value):
    if not value.replace(' ', '').isalpha():
        raise ValidationError(
            _('The field can only contain alphabetic characters.'),
            code='alpha_chars_only'
        )


class AccountBank(models.Model):
    name = models.CharField(max_length=255, verbose_name='Bank Name')
    remarks = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, blank=True, null=True)
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,
                                related_name='bank_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,
                                related_name='bank_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_acc_bank'

    def __str__(self):
        return self.name

class LeaveType(models.Model):
    leave_type_code = models.CharField(max_length=10)
    name = models.CharField(max_length=50, verbose_name='Leave Type Name',validators=[validate_alpha_chars_only])
    max_days = models.IntegerField(blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='leave_type_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='leave_type_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_leave_type'

    def __str__(self):
        return self.name

class Holiday(models.Model):
    name = models.CharField(max_length=50, verbose_name='Holiday Name')
    type = models.ForeignKey(HolidayType,on_delete=models.SET_NULL, verbose_name='Holiday Type',blank=True,null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField(blank=True,null=True)
    end_time = models.TimeField(blank=True,null=True)
    remarks = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='holiday_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='holiday_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_holiday'

    def __str__(self):
        return self.name
