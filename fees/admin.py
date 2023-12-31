from django.contrib import admin
from .models import *

# Register your models here.

class FeesTypeAdmin(admin.ModelAdmin):
    list_display = ['name','code','is_active']
    prepopulated_fields = {'code': ('name',)}
    class Meta:
        model = FeesType

class FeesDiscountAdmin(admin.ModelAdmin):
    list_display = ['name','code','is_active']
    prepopulated_fields = {'code': ('name',)}
    class Meta:
        model = FeesDiscount

admin.site.register(FeesType, FeesTypeAdmin)
admin.site.register(FeesDiscount, FeesDiscountAdmin)