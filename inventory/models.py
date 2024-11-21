from django.db import models
from institution.models import Institution, Branch
from django_userforeignkey.models.fields import UserForeignKey
from django.db.models import UniqueConstraint
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


# Create your models here.
class Warehouse(models.Model):
    CATEGORY = [
        ('FINISHED_GOODS','Finished Goods'),
        ('RAW_MATERIALS',"Raw Materials"),
    ]

    name = models.CharField(max_length=255,verbose_name='Warehouse Name')
    keyword = models.CharField(max_length=255, blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    category = models.CharField(max_length=255, verbose_name='Warehouse Category', choices=CATEGORY)
    as_default = models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Institution Name')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='warehouse_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='warehouse_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inv_warehouse'
        verbose_name = 'Warehouse'
        constraints = [
            UniqueConstraint(fields=['name','is_active','status','institution','branch'], name='warehouse_unique_constraint')
        ] 
    def __str__(self):
        return str(self.name)
    
@receiver(post_save, sender=Warehouse)
def set_as_default(sender, instance, **kwargs):
    if instance.as_default:
        sender.objects.filter(institution=instance.institution, branch=instance.branch,status=True,category=instance.category).exclude(id=instance.id).update(as_default=False)

class Brand(models.Model):
    name = models.CharField(max_length=255,verbose_name='Brand Name')
    keyword = models.CharField(max_length=255,verbose_name='Keyword', blank=True, null=True,editable=False)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Institution Name')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='brand_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='brand_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inv_brand'
        verbose_name = 'Brand'
        constraints = [
            UniqueConstraint(fields=['name','keyword','status','institution','branch'], name='brand_unique_constraint')
        ]

    def save(self, *args, **kwargs):
        if self.name:
            self.keyword = self.name.upper().replace(' ','_').replace('-', '_')
        super(Brand,self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)
    
class Category(models.Model):
    name = models.CharField(max_length=255,verbose_name='Category Name')
    keyword = models.CharField(max_length=255,verbose_name='Keyword', blank=True, null=True,editable=False)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Institution Name')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='category_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='category_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inv_category'
        verbose_name = 'Category'
        constraints = [
            UniqueConstraint(fields=['name','keyword','status','institution','branch'], name='category_unique_constraint')
        ]

    def save(self, *args, **kwargs):
        if self.name:
            self.keyword = self.name.upper().replace(' ','_').replace('-', '_')
        super(Category,self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

class Model(models.Model):
    name = models.CharField(max_length=255,verbose_name='model Name')
    keyword = models.CharField(max_length=255,verbose_name='Keyword', blank=True, null=True,editable=False)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Institution Name')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='model_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='model_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inv_model'
        verbose_name = 'Model'
        constraints = [
            UniqueConstraint(fields=['name','keyword','status','institution','branch'], name='model_unique_constraint')
        ]

    def save(self, *args, **kwargs):
        if self.name:
            self.keyword = self.name.upper().replace(' ','_').replace('-', '_')
        super(Model,self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

class Item(models.Model):
    TYPE = [
        ('FINISHED_GOODS','Finished Goods'),
        ('RAW_MATERIALS',"Raw Materials"),
    ]
    code = models.CharField(max_length=100,verbose_name='Item Code')
    name = models.CharField(max_length=255,verbose_name='Item Name')
    type = models.CharField(max_length=50,choices=TYPE)
    keyword = models.CharField(max_length=255,verbose_name='Keyword', blank=True, null=True,editable=False)
    description = models.TextField(blank=True, null=True, verbose_name='Item Description')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True,verbose_name='Item Category')
    model = models.ForeignKey(Model, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Item Model')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Brand')
    purchase_item = models.BooleanField(default=True)
    purchase_uom = models.CharField(max_length=10,blank=True, null=True)
    def_pur_unit_price = models.DecimalField(blank=True, null=True,verbose_name='Regular Purchase Price',max_digits=10,decimal_places=2)
    min_pur_qty = models.IntegerField(default=1,verbose_name='Min Purchase Qty')
    default_uom = models.CharField(max_length=10, blank=True, null=True)
    default_warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, blank=True, null=True)
    sales_item = models.BooleanField(default=False)
    sales_uom = models.CharField(max_length=10, blank=True, null=True)
    min_sales_qty = models.IntegerField(default=1, verbose_name='Min Sales Qty')
    def_sales_price = models.DecimalField(blank=True, null=True,verbose_name='Default Sales Price',max_digits=10,decimal_places=2)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Institution Name')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='item_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='item_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inv_item'
        verbose_name = 'Item'
        constraints = [
            UniqueConstraint(fields=['name','keyword','status','institution','branch'], name='item_unique_constraint'),
            UniqueConstraint(fields=['code','status','institution','branch'], name='item_code_unique_constraint')
        ]

    def save(self, *args, **kwargs):
        if self.name:
            self.keyword = self.name.upper().replace(' ','_').replace('-', '_')
        super(Item,self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

class StockMaster(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='stock_item')
    item_name = models.CharField(blank=True, null=True, max_length=255)
    uom = models.CharField(max_length=10, verbose_name='UoM',blank=True,null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock_warehose')
    quantity = models.IntegerField(default=0, verbose_name='Stock Quantity')
    book_quantity = models.IntegerField(default=0)
    sefty_alter_qty = models.IntegerField(default=0)
    unit_cost_value = models.DecimalField(blank=True, null=True,verbose_name='Unit Cost Value',max_digits=10,decimal_places=2)
    weighted_unit_cost_value = models.DecimalField(blank=True, null=True,verbose_name='Weighted Unit Cost Value',max_digits=10,decimal_places=2)
    last_receive_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Institution Name')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='stock_mst_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='stock_mst_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inv_stock_master'
        verbose_name = 'Stock'
        constraints = [
            UniqueConstraint(fields=['item','warehouse','status','institution','branch'], name='stock_mast_constraint'),
        ]
    
    def __str__(self):
        return str(self.item)
    
@receiver(pre_save, sender=StockMaster)
def update_item_name(sender, instance, **kwargs):
    if instance.item:
        item_name = Item.objects.get(pk=instance.item.id)
        instance.item_name = item_name.name
        instance.uom = item_name.default_uom

from purchase.models import GoodsReceiptNotesDetails, Supplier

class StockTransaction(models.Model):
    type = models.CharField(max_length=20,verbose_name='Voucher Type')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=50,verbose_name='Invoice No')
    grn_detail = models.ForeignKey(GoodsReceiptNotesDetails, on_delete=models.CASCADE, verbose_name='GRN Details')
    uom = models.CharField(max_length=10, blank=True, null=True, verbose_name='UoM')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='Supplier')
    from_warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL,blank=True, null=True, related_name='stock_trns_from')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock_trns_warhouse')
    trns_date = models.DateTimeField(blank=True, null=True)
    trns_type = models.CharField(max_length=25,verbose_name='Transaction Type')
    quantity = models.IntegerField(default=0)
    vat_amt = models.DecimalField(blank=True, null=True,verbose_name='VAT Amount',max_digits=10,decimal_places=2)
    amount = models.DecimalField(blank=True, null=True,verbose_name='Amount',max_digits=10,decimal_places=2)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Institution Name')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='stock_trns_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='stock_trns_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inv_stock_transaction'
        verbose_name = 'Stock Transaction'
        constraints = [
            UniqueConstraint(fields=['grn_detail','status','institution','branch'], name='stock_trns_constraint'),
        ]

    def __str__(self):
        return str(self.invoice_no)


