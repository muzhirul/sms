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
    fields = ['fees_type','due_date','amount','percentage','fix_amt','is_active','status','institution','branch']
    extra = 1
    show_change_link = True

class FeeDetailsBreakDownTabularInline(admin.TabularInline):
    model = FeeDetailsBreakDown
    fields = ['name','amount','is_active','status','institution','branch']
    extra = 1
    # show_change_link = True

class FeesTransactionDetailTabularInline(admin.TabularInline):
    model = FeesTransactionDetails
    fields = ['student','name','amount','is_active','status','institution','branch']
    extra = 1

class FeesMasterAdmin(admin.ModelAdmin):
    fields = ['class_name','section','group','session','version']
    list_display = ['class_name','group','section','session','version','status']
    search_fields = ['class_name__name','section__section','session__session']

    inlines = [FeesDetailsTabularInline]
    class Meta:
        model = FeesMaster

class FeesTransactionAdmin(admin.ModelAdmin):
    list_display = ['student','fees_detail','pay_method','pay_date','is_active']
    inlines = [FeesTransactionDetailTabularInline]
    class Meta:
        model = FeesTransaction

class FeesDetailsAdmin(admin.ModelAdmin):
    inlines = [FeeDetailsBreakDownTabularInline]
    class Meta:
        model = FeesDetails


admin.site.register(FeesType, FeesTypeAdmin)
admin.site.register(FeesDiscount, FeesDiscountAdmin)
admin.site.register(FeesMaster,FeesMasterAdmin)
admin.site.register(FeesDetails,FeesDetailsAdmin)
admin.site.register(FeesTransaction,FeesTransactionAdmin)