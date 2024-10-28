from django.contrib import admin
from .models import *

# Register your models here.
class ChartofAccountsAdmin(admin.ModelAdmin):
    list_display = ['parent','code', 'coa_type', 'title', 'keyword', 'income_stat_type', 'direct_posting','carry_forward']
    search_fields = ['parent', 'coa_type', 'title', 'keyword', 'income_stat_type', 'direct_posting','carry_forward']
    list_filter = ['parent']

    # save_as = True
    save_on_top = True
    list_per_page = 15

    class Meta:
        model = ChartofAccounts

class AccountPeriodAdmin(admin.ModelAdmin):
    list_display = ['code','start_date','end_date','title','status']
    search_fields = ['code','start_date','end_date','title','status']

    save_on_top = True
    list_per_page = 20

    class Meta:
        model = AccountPeriod

class AccountBanksAdmin(admin.ModelAdmin):
    list_display = ['bank_name','branch_name','account_no','status']
    search_fields = ['bank_name','branch_name','account_no','status']
    list_filter = ['status']

    save_on_top = True
    list_per_page = 20

    class Meta:
        model = AccountBanks

class AccountLedgerAdmin(admin.ModelAdmin):
    list_display = ['voucher_type','gl_date','voucher_no','acc_coa','acc_coa_ref','acc_period','narration','particulars','credit_amt','debit_amt']
    search_fields = ['voucher_type','gl_date','voucher_no','acc_coa','acc_coa_ref','acc_period','narration','particulars','credit_amt','debit_amt']

    class Meta:
        model = AccountLedger

class AccountVoucherDetailsTabularInline(admin.TabularInline):
    model = AccountVoucherDetails
    fields = ['acc_coa','acc_bank','particulars','debit_amt','credit_amt','status','institution','branch']
    extra = 0

class AccountVoucherMasterAdmin(admin.ModelAdmin):
    list_display = ['voucher_type','gl_date','voucher_no','total_debit_amt','total_credit_amt']
    search_fields = ['voucher_type','gl_date','voucher_no','total_debit_amt','total_credit_amt']

    class Meta:
        model = AccountVoucherMaster

    inlines = [AccountVoucherDetailsTabularInline]


admin.site.register(ChartofAccounts, ChartofAccountsAdmin)
admin.site.register(AccountPeriod, AccountPeriodAdmin)
admin.site.register(AccountBanks, AccountBanksAdmin)
admin.site.register(AccountLedger, AccountLedgerAdmin)
admin.site.register(AccountVoucherMaster, AccountVoucherMasterAdmin)