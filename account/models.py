from django.db import models
from institution.models import Institution, Branch
from django_userforeignkey.models.fields import UserForeignKey

# Create your models here.
class ChartofAccounts(models.Model):
    INCOME_STATEMENT = [
        ('Operating','Operating'),
        ('Financial','Financial'),
    ]
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='sub_coa')
    coa_type = models.CharField(max_length=10,verbose_name='COA Type')
    code = models.BigIntegerField(unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    keyword = models.CharField(max_length=255,blank=True,null=True,editable=False)
    income_stat_type = models.CharField(max_length=50,blank=True, null=True, verbose_name='Income Statement Type',choices=INCOME_STATEMENT)
    balance_sheet_type = models.CharField(max_length=50,blank=True,null=True,verbose_name='Balance Sheet Type')
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
