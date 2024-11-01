from django.contrib import admin
from .models import *

# Register your models here.
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name','keyword','description','address','category','as_default','is_active','status']
    search_fields = ['name','keyword','description','address','category','as_default','is_active','status']
    save_on_top = True
    
    class Meta:
        model = Warehouse

admin.site.register(Warehouse, WarehouseAdmin)