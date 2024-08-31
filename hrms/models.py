from django.db import models
from django_userforeignkey.models.fields import UserForeignKey
from institution.models import Institution, Branch
from setup_app.models  import HolidayType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
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

class PayrollElement(models.Model):
    ELEMENT_TYPE = (('Allowance','Allowance'),('Deduction','Deduction'),('Other','Other'))
    name = models.CharField(max_length=255)
    type_name =models.CharField(max_length=255,verbose_name='Type',choices=ELEMENT_TYPE)
    value = models.CharField(max_length=255,blank=True,null=True)
    type = models.IntegerField(blank=True,null=True,editable=False)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='pay_ele_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='pay_ele_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hrms_payroll_elmnt'

    def __str__(self):
        return self.name

@receiver(pre_save, sender=PayrollElement)
def update_element_type(sender, instance, **kwargs):
    if instance.type_name=='Allowance':
        print(instance.type_name)
        instance.type = 1
    elif instance.type_name=='Deduction':
        print(instance.type_name)
        instance.type = -1
    else:
        instance.type = 0

def salary_setup_code():
    last_leave_code = SalarySetupMst.objects.all().order_by('code').last()
    if not last_leave_code or last_leave_code.code is None:
        return 'ST-' + '01'
    leave_num = str(last_leave_code.code)[-2:]
    leave_num_int = int(leave_num)
    new_leave_num = leave_num_int + 1
    new_gd_num = 'ST-' + str(new_leave_num).zfill(2)
    return new_gd_num  

class SalarySetupMst(models.Model):
    code = models.CharField(max_length=255,verbose_name='Salary Setup Code',editable=False,default=salary_setup_code)
    name = models.CharField(max_length=255)
    remarks = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='sal_stp_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='sal_stp_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hrms_salary_setup_mst'
    
    def __str__(self):
        return str(self.name)
    
class SalarySetupDtl(models.Model):
    salary_setup_mst = models.ForeignKey(SalarySetupMst,on_delete=models.SET_NULL,blank=True,null=True,related_name='salary_setup_dtl')
    payroll_ele = models.ForeignKey(PayrollElement,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Element',limit_choices_to={'is_active': 'True'},)
    fixed_amt = models.DecimalField(blank=True, null=True,verbose_name='Fixed Amount',max_digits=8,decimal_places=2)
    formula = models.CharField(max_length=255,blank=True,null=True)
    min_amt = models.DecimalField(blank=True, null=True,verbose_name='Minimum Amount',max_digits=8,decimal_places=2)
    max_amt = models.DecimalField(blank=True, null=True,verbose_name='Max Amount',max_digits=8,decimal_places=2)
    remarks = models.TextField(blank=True, null=True)
    seq_order = models.IntegerField(blank=True, null=True,verbose_name='Ordering')
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='sal_stp_dtl_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='sal_stp_dtl_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hrms_salary_setup_dtl'
    
    def __str__(self):
        return str(self.payroll_ele)
    
@receiver(pre_save, sender=SalarySetupDtl)
def calculate_info(sender, instance, **kwargs):
    if instance.formula:
        context = {
            'gross_pay': 50000,
            'basic_pay':26000,
            'house_rent': 20,
            'medical': 10,
            'convence': 5,
            'others': 5,
        }
        formatted_formula = instance.formula.format(**context)
        import ast
        basic = eval(compile(ast.parse(formatted_formula, mode='eval'), '', 'eval'))
        print((basic))
    else:
        instance.message_body = None

def acc_cost_center_code():
    last_acc_cost_code = AccountCostCenter.objects.all().order_by('code').last()
    if not last_acc_cost_code or last_acc_cost_code.code is None:
        return 'AC-' + '01'
    acc_cost_num = str(last_acc_cost_code.code)[-2:]
    acc_cost_num_int = int(acc_cost_num)
    new_acc_cost_num = acc_cost_num_int + 1
    new_gd_num = 'AC-' + str(new_acc_cost_num).zfill(2)
    return new_gd_num  

class AccountCostCenter(models.Model):
    code = models.CharField(max_length=30,editable=False,default=acc_cost_center_code)
    name = models.CharField(max_length=255,verbose_name='Cost Center Name')
    start_date = models.DateField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Institution Name')
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='Branch Name')
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='acc_cost_center_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='acc_cost_center_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hrms_acc_cost_cetr'

    def __str__(self):
        return str(self.name)