from django.db import models
from institution.models import Institution, Branch
from hrms.models import AccountBank
from setup_app.models import *
from inventory.models import *
from django_userforeignkey.models.fields import UserForeignKey
from django.db.models import UniqueConstraint
from django.db.models import Sum, F
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
    opening_amt = models.DecimalField(default=0,verbose_name='Opening Balance',max_digits=10,decimal_places=2)
    current_amt = models.DecimalField(default=0,verbose_name='Current Balance',max_digits=10,decimal_places=2)
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

class GoodSReceiptNoteMaster(models.Model):
    TYPE = [
        ('LOCAL','Local'),
    ]
    code = models.CharField(max_length=50, blank=True, null=True, verbose_name='GRN Number')
    grn_date = models.DateField(verbose_name='GRN Date')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Receiving Warehouse')
    pay_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, blank=True, null=True)
    purchase_type = models.CharField(max_length=20, choices=TYPE)
    total_rec_qty = models.IntegerField(blank=True, null=True, verbose_name='Total Receive Quantity')
    total_dis_amt = models.DecimalField(blank=True, null=True,verbose_name='Total Discount Amount',max_digits=10,decimal_places=2)
    total_rec_amt = models.DecimalField(blank=True, null=True,verbose_name='Total Receive Amount',max_digits=10,decimal_places=2)
    total_net_amt = models.DecimalField(blank=True, null=True,verbose_name='Total Net Amount',max_digits=10,decimal_places=2)
    remarks = models.TextField(blank=True, null=True)
    confirm_with_pay = models.BooleanField(default=False)
    confirm_without_pay = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='goods_rece_notes_mst_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='goods_rece_notes_mst_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pur_goods_receive_notes_mst'
        verbose_name = 'Goods Receive Notes'
        constraints = [
            UniqueConstraint(fields=['code','status','institution','branch'], name='goods_receive_notes_mst_unique_constraint')
        ]

    def clean(self):
        # Ensure only one of the two fields is True
        if self.pk:
            # Get the current instance from the database to check previous values
            current_instance = GoodSReceiptNoteMaster.objects.get(pk=self.pk)
            if current_instance.confirm_with_pay and not self.confirm_with_pay:
                raise ValidationError("Cannot set 'confirm with pay' to False once it is True.")
            if current_instance.confirm_without_pay and not self.confirm_without_pay:
                raise ValidationError("Cannot set 'confirm without pay' to False once it is True.")
            if current_instance.confirm_with_pay or current_instance.confirm_without_pay:
                raise ValidationError("Updates are not allowed for this record as 'confirm with pay' or 'confirm without pay' is already Done.")

        # Ensure only one of the fields is True
        if self.confirm_with_pay and self.confirm_without_pay:
            raise ValidationError("Only one of 'confirm with pay' or 'confirm without pay' can be True at a time.")

    def save(self, *args, **kwargs):
        # Call the clean method to enforce validation before saving
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.code)
    
@receiver(post_save, sender=GoodSReceiptNoteMaster)
def grn_no_posting(sender, instance, **kwargs):
    if not instance.code:
        new_grn_no = generate_code(instance.institution,instance.branch,'Goods Receipt Note')
        instance.code = new_grn_no
        instance.save()
        

class GoodsReceiptNotesDetails(models.Model):
    goods_receipt_note = models.ForeignKey(GoodSReceiptNoteMaster, on_delete=models.CASCADE, related_name='grn_details')
    line_no = models.IntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    rcv_qty = models.IntegerField()
    rcv_uom = models.CharField(max_length=20, blank=True, null=True)
    rcv_rate = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    rcv_amt = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    net_total_amt = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='goods_rece_notes_dtl_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL,related_name='goods_rece_notes_dtl_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pur_goods_receive_notes_dtl'

    def save(self, *args, **kwargs):
        if self.rcv_qty is not None and self.rcv_rate is not None:
            self.rcv_amt = self.rcv_qty * self.rcv_rate
            self.net_total_amt = self.rcv_qty * self.rcv_rate
        else:
            self.rcv_amt = None
            self.net_total_amt = None
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.item)
    
@receiver(pre_save, sender=GoodsReceiptNotesDetails)
def update_item_name(sender, instance, **kwargs):
    if instance.item:
        item_name = Item.objects.get(pk=instance.item.id)
        instance.item_name = item_name.name
 

@receiver(post_save, sender=GoodSReceiptNoteMaster)
def update_confirm_status(sender, instance, **kwargs):
    if instance.confirm_without_pay:
        try:
            Supplier.objects.filter(status=True, pk=instance.supplier.id,institution=instance.institution, branch=instance.branch).update(current_amt=F('current_amt')+instance.total_net_amt)
        except:
            print('Supplier Not Found..',instance.supplier)
    if instance.confirm_with_pay or instance.confirm_without_pay:
        for grn_detail in GoodsReceiptNotesDetails.objects.filter(goods_receipt_note=instance.id, status=True,institution=instance.institution, branch=instance.branch):
            if StockMaster.objects.filter(status=True,institution=instance.institution, branch=instance.branch,item=grn_detail.item, warehouse=instance.warehouse).exists():
                StockMaster.objects.filter(status=True,item=grn_detail.item, warehouse=instance.warehouse,
                                           institution=instance.institution, branch=instance.branch).update(quantity=F('quantity')+grn_detail.rcv_qty)
            else:
                StockMaster.objects.get_or_create(
                    status=True,
                    institution=instance.institution,
                    branch=instance.branch,
                    item=grn_detail.item,
                    uom=grn_detail.rcv_uom,
                    warehouse=instance.warehouse,
                    defaults={'quantity': grn_detail.rcv_qty}
                )
            from inventory.models import StockTransaction
            if StockTransaction.objects.filter(status=True,institution=instance.institution, branch=instance.branch,item=grn_detail.item,grn_detail=grn_detail):
                print('This is already inserted...........')
            else:
                StockTransaction.objects.get_or_create(
                    status = True,
                    institution=instance.institution,
                    branch=instance.branch,
                    item=grn_detail.item,
                    uom=grn_detail.rcv_uom,
                    warehouse=grn_detail.goods_receipt_note.warehouse,
                    trns_date=grn_detail.updated_at,
                    type='purchase invoice',
                    invoice_no = grn_detail.goods_receipt_note.code,
                    grn_detail = grn_detail,
                    supplier = grn_detail.goods_receipt_note.supplier,
                    trns_type = 'PURCHASE',
                    quantity = grn_detail.rcv_qty,
                    amount = grn_detail.net_total_amt
                )
                

    
@receiver(post_save, sender=GoodsReceiptNotesDetails)
def update_grn_total_amounts(sender, instance, **kwargs):
    # Retrieve the related AccountVoucherMaster instance
    grn_mst = instance.goods_receipt_note
    if grn_mst:
        # Calculate the total debit and credit amounts from GoodsReceiptNotesDetails
        total_rcv_qty = GoodsReceiptNotesDetails.objects.filter(goods_receipt_note=grn_mst,status=True,institution=grn_mst.institution,branch=grn_mst.branch).aggregate(Sum('rcv_qty'))['rcv_qty__sum'] or 0
        total_rcv_amt = GoodsReceiptNotesDetails.objects.filter(goods_receipt_note=grn_mst,status=True,institution=grn_mst.institution,branch=grn_mst.branch).aggregate(Sum('rcv_amt'))['rcv_amt__sum'] or 0
        total_net_amt = GoodsReceiptNotesDetails.objects.filter(goods_receipt_note=grn_mst,status=True,institution=grn_mst.institution,branch=grn_mst.branch).aggregate(Sum('net_total_amt'))['net_total_amt__sum'] or 0

        # Update the totals in GoodsReceiptNotesDetails
        grn_mst.total_rec_qty = total_rcv_qty
        grn_mst.total_rec_amt = total_rcv_amt
        grn_mst.total_net_amt = total_net_amt
        grn_mst.save()
        
