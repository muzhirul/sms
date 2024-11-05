from django.db import models
from institution.models import Institution, Branch
from hrms.models import AccountBank
from setup_app.models import *
from inventory.models import Warehouse
from inventory.models import Item
from django_userforeignkey.models.fields import UserForeignKey
from django.db.models import UniqueConstraint
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from sms.permission import generate_code

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

class PurchaseOrderMaster(models.Model):
    code = models.CharField(max_length=50, blank=True, null=True, verbose_name='Order Number')
    order_date = models.DateField()
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Receiving Warehouse')
    pay_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, blank=True, null=True)
    total_ord_qty = models.IntegerField(blank=True, null=True, verbose_name='Total Order Qty')
    total_dis_amt = models.DecimalField(blank=True, null=True,verbose_name='Total Discount Amount',max_digits=10,decimal_places=2)
    total_ord_amt = models.DecimalField(blank=True, null=True,verbose_name='Total Order Amount',max_digits=10,decimal_places=2)
    remarks = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='pur_ord_mst_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='pur_ord_mst_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pur_order_mst'
        verbose_name = 'Purchase Order'
        constraints = [
            UniqueConstraint(fields=['code','status','institution','branch'], name='pur_ord_mst_unique_constraint')
        ]

    def __str__(self):
        return str(self.order_date)
    
@receiver(post_save, sender=PurchaseOrderMaster)
def purchase_no_posting(sender, instance, **kwargs):
    if not instance.code:
        new_po_no = generate_code(instance.institution,instance.branch,'Purchase')
        instance.code = new_po_no
        instance.save()

class PurchaseOrderDetails(models.Model):
    order_mst = models.ForeignKey(PurchaseOrderMaster, on_delete=models.SET_NULL, blank=True, null=True, related_name='order_details')
    line = models.IntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order_qty = models.IntegerField()
    approve_qty = models.IntegerField(blank=True, null=True)
    receive_qty = models.IntegerField(blank=True, null=True)
    uom = models.CharField(verbose_name='UoM',max_length=20)
    unit_price = models.DecimalField(max_digits=9,decimal_places=2)
    other_cost = models.DecimalField(max_digits=9,decimal_places=2, blank=True, null=True)
    vat_pct = models.DecimalField(max_digits=9,decimal_places=2, blank=True, null=True, verbose_name='VAT %')
    vat_amt = models.DecimalField(max_digits=9,decimal_places=2, blank=True, null=True, verbose_name='VAT Amount')
    dis_pct = models.DecimalField(max_digits=9,decimal_places=2, blank=True, null=True, verbose_name='Discount %')
    dis_amt = models.DecimalField(max_digits=9,decimal_places=2, blank=True, null=True, verbose_name='Discount Amount')
    total_price = models.DecimalField(max_digits=9,decimal_places=2, blank=True, null=True, verbose_name='Total Price')
    net_total_amt = models.DecimalField(max_digits=9,decimal_places=2, blank=True, null=True, verbose_name='Net Total Amount')
    remarks = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='pur_ord_dtl_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='pur_ord_dtl_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pur_order_dtl'

    def __str__(self):
        return str(self.item)
