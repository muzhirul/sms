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


# class Department(models.Model):
#     dept_id = models.CharField(max_length=10)
#     name = models.CharField(max_length=255)
#     sect_id = models.CharField(max_length=10, blank=True, null=True)
#     section_id = models.CharField(max_length=10, blank=True, null=True)
#     status = models.BooleanField(default=True)
#     institution = models.ForeignKey(
#         Institution, on_delete=models.CASCADE, blank=True, null=True)
#     branch = models.ForeignKey(
#         Branch, on_delete=models.CASCADE, blank=True, null=True)
#     created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,
#                                 related_name='dept_creator', editable=False, blank=True, null=True)
#     updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,
#                                 related_name='depat_update_by', editable=False, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'hr_department'

#     def __str__(self):
#         return self.name

class Desig(models.Model):
    desig_id = models.CharField(max_length=10)
    name = models.CharField(max_length=255, verbose_name='Designation Name')
    dgroup_id = models.CharField(max_length=10, blank=True, null=True)
    sdate = models.DateField(blank=True, null=True)
    attn = models.IntegerField(blank=True, null=True)
    holiday_allow = models.BooleanField(default=True)
    night_allow = models.BooleanField(default=False)
    tiffin_allow = models.BooleanField(default=False)
    festival_allow = models.BooleanField(default=True)
    sal_grade = models.IntegerField(blank=True, null=True)
    work_type = models.CharField(max_length=255, blank=True, null=True)
    ifter_allow = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, blank=True, null=True)
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,
                                related_name='degi_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,
                                related_name='degi_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_desig'

    def __str__(self):
        return self.name


class ElPayment(models.Model):
    emp_id = models.CharField(max_length=20, blank=True, null=True)
    days = models.IntegerField(blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    pay_for_year = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'hr_el_payment'

    def __str__(self):
        return str(self.id)
