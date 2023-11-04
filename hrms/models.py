from hashlib import blake2b
from importlib.abc import Traversable
from django.db import models
from django_userforeignkey.models.fields import UserForeignKey
from institution.models import Institution, Branch

# Create your models here.


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


class AttendanceRaw(models.Model):
    mach_no = models.CharField(max_length=3, blank=True, null=True)
    card_no = models.CharField(max_length=50)
    atnd_date = models.DateField()
    atnd_time = models.TimeField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_atnd_raw'

    def __str__(self):
        return self.card_no


class AttendanceDetail(models.Model):
    att_date = models.DateField()
    emp_no = models.CharField(max_length=20)
    in_time = models.TimeField()
    in_time2 = models.TimeField()
    late = models.IntegerField()
    late2 = models.IntegerField()
    status = models.BooleanField(default=True)
    status2 = models.BooleanField(default=True)
    out_time = models.TimeField()
    out_time2 = models.TimeField()
    ot_hour = models.IntegerField()
    ot_hour2 = models.IntegerField()
    extra_ot = models.IntegerField()
    manul_att = models.CharField(max_length=50, blank=True, null=True)
    manual_status = models.CharField(max_length=50, blank=True, null=True)
    deduct_val = models.IntegerField(blank=True, null=True)
    nor_ot = models.IntegerField(blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    shift_code = models.CharField(max_length=20, blank=True, null=True)
    is_late_grant = models.BooleanField(default=False)
    is_early_packup_grant = models.BooleanField(default=False)
    is_deviation_grant = models.BooleanField(default=False)
    com_id = models.IntegerField(blank=True, null=True)
    others3 = models.IntegerField(blank=True, null=True)
    out_time3 = models.TimeField(blank=True, null=True)
    row_status = models.CharField(max_length=255, blank=True, null=True)
    others4 = models.IntegerField(blank=True, null=True)
    out_time4 = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_attendance_details'

    def __str__(self):
        return str(self.id)
