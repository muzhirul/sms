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

admin.site.register(Supplier,SupplierAdmin)