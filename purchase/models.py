from django.db import models
from institution.models import Institution, Branch
from hrms.models import AccountBank
from setup_app.models import *
from django_userforeignkey.models.fields import UserForeignKey
from django.db.models import UniqueConstraint
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Create your models here.
class Supplier(models.Model):
    TYPE = [
        ('Manufacturer','Manufacturer'),
        ('Importer',"Importer"),
        ('Trader',"Trader"),
        ('Local',"Local"),
    ]
    code = models.CharField(max_length=20, blank=True, null=True, verbose_name='Supplier Code')
    name = models.CharField(max_length=255, verbose_name='Supplier Name')
    short_name = models.CharField(max_length=50, verbose_name='Supplier Short Name')
    address = models.TextField()
    owner_name = models.CharField(max_length=255,blank=True, null=True, verbose_name='Owner Name')
    owner_email = models.EmailField(blank=True, null=True, verbose_name='Owner Email')
    owner_phone_number = models.CharField(max_length=20, verbose_name='Phone Number', blank=True, null=True)
    phone_number = models.CharField(max_length=20, verbose_name='Phone Number')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    opening_amt = models.DecimalField(blank=True, null=True,verbose_name='Opening Balance',max_digits=10,decimal_places=2)
    current_amt = models.DecimalField(blank=True, null=True,verbose_name='Current Balance',max_digits=10,decimal_places=2)
    con_person = models.CharField(max_length=255, blank=True, null=True, verbose_name='Contact Person Name')
    con_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Phone Number')
    con_email = models.EmailField(max_length=255, blank=True, null=True, verbose_name='Email')
    type = models.CharField(max_length=20,verbose_name='Supplier Type', choices=TYPE)
    owner_nid = models.CharField(max_length=50,blank=True,null=True, verbose_name='Owner NID')
    bin = models.CharField(max_length=20,blank=True, null=True, verbose_name='BIN Number')
    tin = models.CharField(max_length=50, blank=True, null=True, verbose_name='TIN Number')
    bank = models.ForeignKey(AccountBank, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Bank Name')
    branch_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Bank Branch Name')
    account_number = models.CharField(max_length=100, blank=True, null=True,verbose_name='Bank Account No.')
    last_trns_date = models.DateTimeField(blank=True, null=True, verbose_name='Last Transaction Date')
    thana = models.ForeignKey(Thana, on_delete=models.SET_NULL, blank=True, null=True) 
    district = models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True) 
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, blank=True, null=True) 
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True) 
    is_active= models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Institution Name')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='supplier_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='supplier_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pur_supplier'
        constraints = [
            UniqueConstraint(fields=['name','bin','status','institution','branch'], name='supplier_unique_constraint'),
        ]

    def __str__(self):
        return str(self.name)

