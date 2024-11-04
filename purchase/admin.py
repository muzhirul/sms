from django.contrib import admin
from .models import *

# Register your models here.

class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name','short_name','address','owner_name','phone_number','email']
    search_fields = ['name','short_name','address','owner_name','phone_number','email']

    class Meta:
        model = Supplier

admin.site.register(Supplier,SupplierAdmin)