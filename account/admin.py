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
    list_display = ['code','start_date','end_date','title']
    search_fields = ['code','start_date','end_date','title']

    save_on_top = True
    list_per_page = 20

    class Meta:
        model = AccountPeriod

admin.site.register(ChartofAccounts, ChartofAccountsAdmin)
admin.site.register(AccountPeriod, AccountPeriodAdmin)