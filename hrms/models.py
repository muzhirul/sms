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
