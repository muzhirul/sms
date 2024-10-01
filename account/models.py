from django.db import models
from institution.models import Institution, Branch
from django_userforeignkey.models.fields import UserForeignKey
from django.core.exceptions import ValidationError
from authentication.models import Authentication

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
    ]
    gl_date = models.DateField()
    voucher_type = models.CharField(max_length=30,choices=VOUCHER_TYPE)
    acc_coa = models.ForeignKey(ChartofAccounts,on_delete=models.SET_NULL,blank=True,null=True,related_name='acc_coa')
    acc_coa_ref = models.ForeignKey(ChartofAccounts, on_delete=models.SET_NULL, blank=True,null=True,related_name='acc_ref_coa')
    acc_period = models.ForeignKey(AccountPeriod, on_delete=models.SET_NULL, blank=True,null=True)
    credit_amt = models.DecimalField(blank=True, null=True,max_digits=10,decimal_places=2,verbose_name='Credit Amount')
    debit_amt = models.DecimalField(blank=True, null=True,max_digits=10,decimal_places=2, verbose_name='Debit Amount')
    narration = models.TextField(blank=True,null=True)
    ref_source = models.CharField(max_length=100,blank=True, null=True)
    particulars = models.TextField(blank=True, null=True)
    user = models.OneToOneField(Authentication,on_delete=models.SET_NULL, blank=True,null=True)
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
        return self.gl_date

