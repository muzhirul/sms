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

class FeesDetailsTabularInline(admin.TabularInline):
    model = FeesDetails
    fields = ['fees_type','due_date','amount','fine_type','percentage','fix_amt','is_active','status','institution','branch']
    extra = 1

class FeesMasterAdmin(admin.ModelAdmin):
    fields = ['class_name','section','group','session','version']
    list_display = ['class_name','group','section','session','version','status']
    search_fields = ['class_name__name','section__section','session__session']

    inlines = [FeesDetailsTabularInline]
    class Meta:
        model = FeesMaster

admin.site.register(FeesType, FeesTypeAdmin)
admin.site.register(FeesDiscount, FeesDiscountAdmin)
admin.site.register(FeesMaster,FeesMasterAdmin)