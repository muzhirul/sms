from django.contrib import admin
from .models import *

# Register your models here.

class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name','short_name','address','owner_name','phone_number','email']
    search_fields = ['name','short_name','address','owner_name','phone_number','email']
    fieldsets = [
        ("Basic Information",{'fields':[('code','name','short_name'),
                                        ('type','tin','bin'),
                                        ('phone_number','email')]}),
        ("Owner Information",{'fields':[('owner_name','owner_phone_number',),
                                        ('owner_email','owner_nid') ]}),
        ("Contact Person Information",{'fields':[('con_person','con_number','con_email')]}),
        ("Financial Information",{'fields':[('bank','branch_name','account_number'),
                                            ('opening_amt','current_amt')]}),
        ("Contact Information",{'fields':[('thana','district','division'),
                                          ('country','address')]}),
        ("Other Information",{'fields':[('institution','branch','is_active','status'),
                                        ]})     
    ]

    class Meta:
        model = Supplier

class PurchaseOrderDetailsTabularInline(admin.TabularInline):
    model = PurchaseOrderDetails
    fields = ['line','item','order_qty','approve_qty','receive_qty','uom','unit_price','dis_pct','dis_amt','total_price','net_total_amt','remarks']
    extra = 0

class PurchaseOrderMasterAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Purchase Order",{'fields':[('order_date','supplier','warehouse'),
                                     ('pay_method','remarks','is_active','status'),
                                     ('institution','branch')]})
    ]
    list_display = ['code','order_date','supplier','warehouse','pay_method','total_ord_qty','total_ord_amt','is_active','status']
    search_fields = ['code','order_date','supplier','warehouse','pay_method','total_ord_qty','total_ord_amt','is_active','status']

    inlines = [PurchaseOrderDetailsTabularInline]

    class Meta:
        model = PurchaseOrderMaster

admin.site.register(Supplier,SupplierAdmin)
admin.site.register(PurchaseOrderMaster, PurchaseOrderMasterAdmin)