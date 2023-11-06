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
    list_display = ['name', 'type', 'year', 'status']

    class Meta:
        model = Holiday


admin.site.register(AccountBank, AccountBankAdmin)
admin.site.register(LeaveType, LeaveTypeAdmin)
admin.site.register(Holiday, HolidayAdmin)
