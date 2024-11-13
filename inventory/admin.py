from django.contrib import admin
from .models import *

# Register your models here.
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name','keyword','description','address','category','as_default','is_active','status']
    search_fields = ['name','keyword','description','address','category','as_default','is_active','status']
    save_on_top = True
    
    class Meta:
        model = Warehouse

class BrandAdmin(admin.ModelAdmin):
    list_display = ['name','keyword','description','is_active','status']
    search_fields = ['name','keyword','description','is_active','status']

    class Meta:
        model = Brand

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','keyword','description','is_active','status']
    search_fields = ['name','keyword','description','is_active','status']

    class Meta:
        model = Category

class ModelAdmin(admin.ModelAdmin):
    list_display = ['name','keyword','description','is_active','status']
    search_fields = ['name','keyword','description','is_active','status']

    class Meta:
        model = Model

class ItemAdmin(admin.ModelAdmin):
    list_display = ['name','keyword','description','is_active','status']
    search_fields = ['name','keyword','description','is_active','status']

    class Meta:
        model = Item

class StockMasterAdmin(admin.ModelAdmin):
    list_display = ['item','uom','warehouse','quantity','book_quantity','sefty_alter_qty','unit_cost_value','weighted_unit_cost_value','last_receive_date','is_active','status']
    search_fields = ['item','uom','warehouse','quantity','book_quantity','sefty_alter_qty','unit_cost_value','weighted_unit_cost_value','last_receive_date','is_active','status']
    list_filter = ['item','uom','warehouse']

    class Meta:
        model = StockMaster

class StockTransactionAdmin(admin.ModelAdmin):
    class Meta:
        model = StockTransaction

admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(StockMaster, StockMasterAdmin)
admin.site.register(StockTransaction, StockTransactionAdmin)