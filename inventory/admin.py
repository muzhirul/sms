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

admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Model, ModelAdmin)