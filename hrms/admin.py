from django.contrib import admin
from .models import *
# Register your models here.

class AccountBankAdmin(admin.ModelAdmin):
    list_display = ['name', 'status']

    class Meta:
        model = AccountBank

class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ['leave_type_code', 'name', 'max_days', 'status']

    class Meta:
        model = LeaveType

class HolidayAdmin(admin.ModelAdmin):
    list_display = ['name','type','start_date','end_date','start_time','end_time','is_active','status']

    class Meta:
        model = Holiday

class PayrollElementAdmin(admin.ModelAdmin):
    list_display = ['name','type_name','type','status']

    class Meta:
        model = PayrollElement

class SalarySetupDtlTabularInline(admin.TabularInline):
    model = SalarySetupDtl
    fields = ['seq_order','payroll_ele','fixed_amt','formula','min_amt','max_amt','remarks','status','institution','branch']
    extra = 0

class AccountTaxDtlTabularInline(admin.TabularInline):
    model = AccountTaxDtl
    fields = ['phase','name','lmt','pct','start_date','end_date','status','institution','branch']
    extra = 0

class SalarySetupMstAdmin(admin.ModelAdmin):
    list_display = ['code','name','status']
    search_fields = ['code','name','status']
    inlines = [SalarySetupDtlTabularInline]
    save_on_top = True

    class Meta:
        model = SalarySetupMst


class AccountCostCenterAdmin(admin.ModelAdmin):
    list_display = ['code','name','status']
    search_fields = ['code','name','status']
    save_on_top = True

    class Meta:
        model = AccountCostCenter

class AccountTaxMstAdmin(admin.ModelAdmin):
    list_display = ['code','name','tax_year','status']
    search_fields = ['code','name','tax_year','status']
    inlines = [AccountTaxDtlTabularInline]
    save_on_top = True

    class Meta:
        model = AccountTaxMst

admin.site.register(AccountBank, AccountBankAdmin)
admin.site.register(LeaveType, LeaveTypeAdmin)
admin.site.register(Holiday, HolidayAdmin)
admin.site.register(PayrollElement, PayrollElementAdmin)
admin.site.register(SalarySetupMst, SalarySetupMstAdmin)
admin.site.register(AccountCostCenter, AccountCostCenterAdmin)
admin.site.register(AccountTaxMst, AccountTaxMstAdmin)
