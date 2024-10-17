from django.db import models
from institution.models import Institution, Branch
from academic.models import *
from student.models import *
from account.models import *
from django_userforeignkey.models.fields import UserForeignKey
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from datetime import datetime
from django.db.models import Sum

def validate_alpha_chars_only(value):
    if not value.replace(' ', '').isalpha():
        raise ValidationError(
            _('The field can only contain alphabetic characters.'),
            code='alpha_chars_only'
        )

# Create your models here.
class FeesType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Fees Type Name',validators=[validate_alpha_chars_only])
    code = models.SlugField(max_length=255)
    description = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='fees_type_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='fees_type_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fe_fees_type'

    def __str__(self):
        return str(self.name)
    
class FeesDiscount(models.Model):
    name = models.CharField(max_length=255, verbose_name='Fees Name Discount',validators=[validate_alpha_chars_only])
    code = models.SlugField(max_length=255)
    percentage = models.DecimalField(blank=True, null=True,verbose_name='Discount %',max_digits=4,decimal_places=2)
    amount = models.PositiveIntegerField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    remarks= models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='fees_discount_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='fees_discount_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fe_fees_discount'
        constraints = [
            models.CheckConstraint(check=models.Q(percentage__gte='0'), name='discount_pct_non_negative'),
        ]

    def __str__(self):
        return str(self.name)
    
class FeesMaster(ClassSection):

    class Meta:
        proxy = True
        verbose_name = 'Fees Master'

class FeesDetails(models.Model):
    FINE_TYPE = ((0,'None'),(1,'Percentage'),(2,'Fix Amount'))
    fees_master = models.ForeignKey(FeesMaster, on_delete=models.CASCADE, related_name='fees_detail')
    fees_type = models.ForeignKey(FeesType,on_delete=models.CASCADE)
    due_date = models.DateField(blank=True,null=True,verbose_name='Due Date')
    amount = models.DecimalField(blank=True, null=True,verbose_name='Amount',max_digits=10,decimal_places=2)
    # fine_type = models.IntegerField(blank=True,null=True,choices=FINE_TYPE)
    percentage = models.DecimalField(blank=True, null=True,verbose_name='Percentage %',max_digits=10,decimal_places=2)
    fix_amt = models.IntegerField(blank=True,null=True, verbose_name='Fix Amount')
    description = models.TextField(blank=True,null=True)
    remarks= models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='fees_dtl_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='fees_dtl_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fe_fees_dtl'

    def __str__(self):
        return f"{self.id}. {self.fees_type}"
    
class FeeDetailsBreakDown(models.Model):
    fees_detail = models.ForeignKey(FeesDetails, on_delete=models.CASCADE, related_name='detail_break_down')
    name = models.CharField(max_length=255,verbose_name='Name')
    amount = models.IntegerField()
    remarks = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='fees_dtl_br_dw_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='fees_dtl_br_dw_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fees_dtl_break_down'

    def __str__(self):
        return f"{self.id}. {self.name}"
    
# @receiver(post_save, sender=FeeDetailsBreakDown)
# def calculate_total_amt(sender, instance, **kwargs):
#     if instance.status and instance.is_active:
#         total_amt = FeeDetailsBreakDown.objects.filter(status=True,is_active=True,fees_detail=instance.fees_detail).aaggregate(total_amt=Sum('amount'))
#         # Accessing the total amount, but handling the case where total_amt might be None
#         total_value = total_amt['total_amt'] if total_amt['total_amt'] is not None else 0

#     # You can now print or return total_value
#     print(total_value)
@receiver(post_save, sender=FeeDetailsBreakDown)
def calculate_total_amt(sender, instance, **kwargs):
    if instance.status and instance.is_active:
        total_amt = FeeDetailsBreakDown.objects.filter(
            status=True,
            is_active=True,
            fees_detail=instance.fees_detail,
            institution = instance.institution,
            branch = instance.branch
        ).aggregate(total_amt=Sum('amount'))
        # Handle the case where total_amt might be None
        total_value = total_amt['total_amt'] if total_amt['total_amt'] is not None else 0
        # You can now print or return total_value
        FeesDetails.objects.filter(status=True,is_active=True,institution = instance.institution,branch = instance.branch,id=instance.fees_detail.id).update(
            amount=total_value
        )
    


class FeesTransaction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True,related_name='fees_trns')
    fees_detail = models.ForeignKey(FeesDetails, on_delete=models.SET_NULL, blank=True,null=True)
    payment_id = models.CharField(max_length=100,blank=True,null=True)
    pay_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL,blank=True,null=True, verbose_name='Payment Method')
    pay_date = models.DateField(blank=True,null=True, verbose_name='Payment Date')
    discount_type = models.ForeignKey(FeesDiscount, on_delete=models.SET_NULL,blank=True,null=True)
    discount_amt = models.DecimalField(blank=True, null=True,verbose_name='Discount Amount',max_digits=8,decimal_places=2)
    fine_amt = models.DecimalField(blank=True, null=True,verbose_name='Fine Amount',max_digits=8,decimal_places=2)
    fees_amt = models.DecimalField(blank=True, null=True,verbose_name='Fees Amount',max_digits=8,decimal_places=2)
    pay_status = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='fees_trns_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='fees_trns_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fees_transaction'

    def __str__(self):
        return str(self.id)
    
    def fees_amount(self):
        return self.fees_detail.amount
    
    def fine_amount(self):
        current_date = datetime.now().date()
        if self.fees_detail.due_date < current_date:
            if self.fees_detail.percentage is not None and self.fees_detail.percentage > 0:
                total_fine =  (round(self.fees_detail.amount*(self.fees_detail.percentage/100)))
            else:
                total_fine = self.fees_detail.fix_amt
        else:
            total_fine = 0
        return total_fine
    
    def discount_amount(self):
        if self.discount_type:
            if self.discount_type.percentage is not None and self.discount_type.percentage > 0:
                discount_amt = round( (self.fees_amount() + self.fine_amount()) * (self.discount_type.percentage/100))
            else:
                discount_amt = (self.discount_type.amount)
        else:
            discount_amt = 0
        
        return discount_amt
    
    def net_fess_amt(self):
        return (self.fees_amount() + self.fine_amount()) - self.discount_amount()



@receiver(pre_save, sender=FeesTransaction)
def calculate_discount_amt(sender, instance, **kwargs):
    current_date = datetime.now().date()
    discount_amt = 0
    if instance.discount_type and instance.pay_status==False:
        if instance.discount_type.percentage is not None and instance.discount_type.percentage > 0:
            discount_amt = round(instance.fees_detail.amount * (instance.discount_type.percentage/100))
        elif instance.discount_type.amount is not None and instance.discount_type.amount > 0:
            discount_amt = instance.discount_type.amount
        else:
            discount_amt = 0
        instance.discount_amt = discount_amt
    if instance.discount_type is None:
        instance.discount_amt = discount_amt
    if instance.fees_detail and instance.pay_status==False:
        instance.fees_amt = instance.fees_detail.amount

@receiver(post_save, sender=FeesTransaction)
def fees_account_posting(sender, instance, **kwargs):
    if instance.pay_status and instance.net_fess_amt() > 0:
        print(instance.net_fess_amt())
        acc_coa = ChartofAccounts.objects.filter(status=True,coa_type='ASSET',title__iexact='Cash In Hand',institution=instance.institution,branch=instance.branch).last()
        acc_coa_ref = ChartofAccounts.objects.filter(status=True,coa_type='INCOME',title__iexact='Service Income',institution=instance.institution,branch=instance.branch).last()
        print(acc_coa,acc_coa_ref)
        from datetime import datetime
        gl_date = datetime.now().strftime('%Y-%m-%d')
        acc_period = AccountPeriod.objects.filter(status=True,start_date__lte=gl_date,end_date__gte=gl_date).last()
        user_info = Authentication.objects.filter(username=instance.student.student_no,institution=instance.institution,branch=instance.branch).last()
        print(acc_period,user_info)
        acc_ledger_dbt_count = AccountLedger.objects.filter(status=True,institution=instance.institution,debit_amt=instance.net_fess_amt(),acc_period=acc_period,
                                                            voucher_type='RECEIVE',acc_coa=acc_coa,acc_coa_ref=acc_coa_ref,
                                                            branch=instance.branch,user=user_info,ref_source='fees_transaction',ref_no=instance.id).count()
        print(acc_ledger_dbt_count)
        if acc_ledger_dbt_count == 0:
            acc_dbt_ledger = {}
            acc_dbt_ledger['gl_date'] = gl_date
            acc_dbt_ledger['voucher_type'] = 'RECEIVE'
            acc_dbt_ledger['acc_coa'] = acc_coa
            acc_dbt_ledger['acc_coa_ref'] = acc_coa_ref
            acc_dbt_ledger['acc_period'] = acc_period
            acc_dbt_ledger['credit_amt'] = 0
            acc_dbt_ledger['debit_amt'] = instance.net_fess_amt()
            acc_dbt_ledger['narration'] = f"Fees Collection from stuent No: {instance.student.student_no}, Name: {instance.student.first_name}"
            acc_dbt_ledger['ref_source'] = 'fees_transaction'
            acc_dbt_ledger['ref_no'] = instance.id
            acc_dbt_ledger['particulars'] = f"Fees Collection"
            acc_dbt_ledger['user'] = user_info
            acc_dbt_ledger['institution'] = instance.institution
            acc_dbt_ledger['branch'] = instance.branch
            acc_dbt = AccountLedger.objects.create(**acc_dbt_ledger)
            print(acc_dbt_ledger)

        acc_ledger_cr_count = AccountLedger.objects.filter(status=True,institution=instance.institution,credit_amt=instance.net_fess_amt(),acc_period=acc_period,
                                                            voucher_type='RECEIVE',acc_coa=acc_coa_ref,acc_coa_ref=acc_coa,
                                                            branch=instance.branch,user=user_info,ref_source='fees_transaction',ref_no=instance.id).count()
        
        if acc_ledger_cr_count == 0:
            acc_cr_ledger = {}
            acc_cr_ledger['gl_date'] = gl_date
            acc_cr_ledger['voucher_type'] = 'RECEIVE'
            acc_cr_ledger['acc_coa'] = acc_coa_ref
            acc_cr_ledger['acc_coa_ref'] = acc_coa
            acc_cr_ledger['acc_period'] = acc_period
            acc_cr_ledger['credit_amt'] = instance.net_fess_amt()
            acc_cr_ledger['debit_amt'] = 0
            acc_cr_ledger['narration'] = f"Fees Collection from stuent No: {instance.student.student_no}, Name: {instance.student.first_name}"
            acc_cr_ledger['ref_source'] = 'fees_transaction'
            acc_cr_ledger['ref_no'] = instance.id
            acc_cr_ledger['particulars'] = f"Fees Collection"
            acc_cr_ledger['user'] = user_info
            acc_cr_ledger['institution'] = instance.institution
            acc_cr_ledger['branch'] = instance.branch
            acc_cr = AccountLedger.objects.create(**acc_cr_ledger)
            print(acc_cr_ledger)

        print('okay...................')

        
    
class FeesTransactionDetails(models.Model):
    fee_trns = models.ForeignKey(FeesTransaction,on_delete=models.CASCADE,verbose_name='Fees Transaction')
    student = models.ForeignKey(Student,on_delete=models.SET_NULL,blank=True,null=True)
    name = models.CharField(max_length=255,verbose_name='Name')
    amount = models.IntegerField()
    remarks = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='fees_trns_dtl_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='fees_trns_dtl_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fees_transaction_dtl'

    def __str__(self):
        return f"{self.id}. {self.name}"

@receiver(post_save, sender=FeesDetails)
def calculate_fine_amt(sender, instance, **kwargs):
    current_date = datetime.now().date()
    fine_amt = 0
    if instance.due_date < current_date:
        if instance.percentage is not None and instance.percentage > 0:
            fine_amt = (round(instance.amount*(instance.percentage/100)))
        else:
            fine_amt = instance.fix_amt
    FeesTransaction.objects.filter(status=True,pay_status=False,fees_detail=instance.id).update(
        fine_amt = fine_amt,
        fees_amt = instance.amount
    )
  

