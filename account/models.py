from django.db import models
from institution.models import Institution, Branch
from django_userforeignkey.models.fields import UserForeignKey
from django.core.exceptions import ValidationError
from authentication.models import Authentication
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from sms.permission import generate_code
from django.db.models import Sum

# Create your models here.
class ChartofAccounts(models.Model):
    INCOME_STATEMENT = [
        ('Operating','Operating'),
        ('Financial','Financial'),
    ]
    FINANCIAL_STATEMENT = [
        ('BALANCE','Balance Sheet'),
        ('INCOME','Income Sheet'),
    ]
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='sub_coa')
    coa_type = models.CharField(max_length=10,verbose_name='COA Type')
    code = models.BigIntegerField(unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    keyword = models.CharField(max_length=255,blank=True,null=True,editable=False)
    income_stat_type = models.CharField(max_length=50,blank=True, null=True, verbose_name='Income Statement Type',choices=INCOME_STATEMENT)
    balance_sheet_type = models.CharField(max_length=50,blank=True,null=True,verbose_name='Balance Sheet Type')
    fin_stat_type = models.CharField(max_length=50,blank=True, null=True, verbose_name='Financial Statement',choices=FINANCIAL_STATEMENT)
    direct_posting = models.BooleanField(default=False)
    carry_forward = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Institution Name')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='acc_coa_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='acc_coa_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'acc_coa'
        verbose_name = 'Chart Of Accounts'

    def save(self, *args, **kwargs):
        self.coa_type = self.coa_type.upper()
        if self.title:
            self.keyword = self.title.replace(' ','_').replace('-', '_')
        super(ChartofAccounts,self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class AccountPeriod(models.Model):
    code = models.CharField(max_length=50,blank=True,null=True, editable=False)
    start_date = models.DateField()
    end_date = models.DateField()
    title = models.CharField(max_length=255) 
    status = models.BooleanField(default=True)
    # institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Institution Name')
    # branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='acc_p_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='acc_p_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'acc_period'
        verbose_name = 'Account Period'

    def __str__(self):
        return self.title
    
    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError({'end_date': 'End date must be greater than start date.'})
    
    def save(self, *args, **kwargs):
        self.clean()
        # Format the code as MMYY-MMYY based on the start_date and end_date
        if self.start_date and self.end_date:
            start_code = self.start_date.strftime('%m%y')
            end_code = self.end_date.strftime('%m%y')
            self.code = f'{start_code}-{end_code}'
        # Call the parent class's save method to ensure the object is saved
        super().save(*args,**kwargs)

class AccountBanks(models.Model):
    bank_name = models.CharField(max_length=255)
    branch_name = models.CharField(max_length=255, blank=True, null=True)
    account_no = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Institution Name')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='acc_ba_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='acc_ba_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'acc_banks'
        verbose_name = 'Account Bank'

    
    def __str__(self):
        return self.account_no

class AccountLedger(models.Model):
    VOUCHER_TYPE = [
        ('PAYMENT','Payment'),
        ('RECEIVE','Receive'),
        ('JOURNAL','Journal'),
    ]
    gl_date = models.DateField()
    voucher_no = models.CharField(blank=True,null=True, max_length=50)
    voucher_type = models.CharField(max_length=30,choices=VOUCHER_TYPE)
    acc_coa = models.ForeignKey(ChartofAccounts,on_delete=models.SET_NULL,blank=True,null=True,related_name='acc_coa')
    acc_coa_ref = models.ForeignKey(ChartofAccounts, on_delete=models.SET_NULL, blank=True,null=True,related_name='acc_ref_coa')
    acc_period = models.ForeignKey(AccountPeriod, on_delete=models.SET_NULL, blank=True,null=True)
    credit_amt = models.DecimalField(blank=True, null=True,max_digits=10,decimal_places=2,verbose_name='Credit Amount')
    debit_amt = models.DecimalField(blank=True, null=True,max_digits=10,decimal_places=2, verbose_name='Debit Amount')
    narration = models.TextField(blank=True,null=True)
    ref_source = models.CharField(max_length=100,blank=True, null=True)
    ref_no = models.IntegerField(blank=True,null=True)
    particulars = models.TextField(blank=True, null=True)
    user = models.ForeignKey(Authentication,on_delete=models.SET_NULL, blank=True,null=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Institution Name')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='acc_le_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='acc_le_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'acc_ledger'
        verbose_name = 'Account Ledger'

    def __str__(self):
        return f"{self.gl_date.strftime('%Y-%m-%d')} - COA ID: {self.acc_coa_id}"

class AccountVoucherMaster(models.Model):
    VOUCHER_TYPE = [
        ('PAYMENT','Payment'),
        ('RECEIVE','Receive'),
        ('JOURNAL','Journal'),
    ]
    voucher_no = models.CharField(blank=True,null=True, max_length=50,editable=False)
    voucher_type = models.CharField(max_length=30,choices=VOUCHER_TYPE)
    gl_date = models.DateField(auto_now_add=True)
    total_debit_amt = models.DecimalField(blank=True, null=True,max_digits=10,decimal_places=2,verbose_name='Total Debit Amount')
    total_credit_amt = models.DecimalField(blank=True, null=True,max_digits=10,decimal_places=2,verbose_name='Total Credit Amount')
    confirm = models.BooleanField(default=False)
    remarks = models.TextField(blank=True,null=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Institution Name')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='acc_vou_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='acc_vou_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'acc_voucher_mst'

    def __str__(self):
        return f"{self.gl_date} - Voucher No: {self.voucher_no}"
    
@receiver(post_save, sender=AccountVoucherMaster)
def voucher_no_posting(sender, instance, **kwargs):
    if instance.voucher_type and not instance.voucher_no:
        new_voucher_no = generate_code(instance.institution,instance.branch,instance.voucher_type)
        instance.voucher_no = new_voucher_no
        instance.save()

    
class AccountVoucherDetails(models.Model):
    line_no = models.IntegerField()
    acc_voucher_mst = models.ForeignKey(AccountVoucherMaster, on_delete=models.SET_NULL,blank=True,null=True,related_name='acc_voucher_detail')
    acc_coa = models.ForeignKey(ChartofAccounts, on_delete=models.SET_NULL, blank=True,null=True)
    acc_bank = models.ForeignKey(AccountBanks, on_delete=models.SET_NULL, blank=True,null=True)
    debit_amt = models.DecimalField(blank=True, null=True,max_digits=10,decimal_places=2, verbose_name='Debit Amount')
    credit_amt = models.DecimalField(blank=True, null=True,max_digits=10,decimal_places=2,verbose_name='Credit Amount')
    particulars = models.TextField(blank=True,null=True)
    narration = models.TextField(blank=True,null=True)
    remarks = models.TextField(blank=True,null=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Institution Name')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='acc_vou_dtl_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='acc_vou_dtl_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'acc_voucher_dtl'

    def __str__(self):
        return f"{self.acc_voucher_mst.voucher_no}"
    
@receiver(post_save, sender=AccountVoucherDetails)
def update_total_amounts(sender, instance, **kwargs):
    # Retrieve the related AccountVoucherMaster instance
    voucher_master = instance.acc_voucher_mst

    if voucher_master:
        # Calculate the total debit and credit amounts from AccountVoucherDetails
        total_debit = AccountVoucherDetails.objects.filter(acc_voucher_mst=voucher_master).aggregate(Sum('debit_amt'))['debit_amt__sum'] or 0
        total_credit = AccountVoucherDetails.objects.filter(acc_voucher_mst=voucher_master).aggregate(Sum('credit_amt'))['credit_amt__sum'] or 0

        # Update the totals in AccountVoucherMaster
        voucher_master.total_debit_amt = total_debit
        voucher_master.total_credit_amt = total_credit
        voucher_master.save()
