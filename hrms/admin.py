from django.contrib import admin
from .models import *
# Register your models here.


class AccountBankAdmin(admin.ModelAdmin):
    list_display = ['name', 'status']

    class Meta:
        model = AccountBank


class AttendanceRawAdmin(admin.ModelAdmin):
    list_display = ['card_no', 'atnd_date', 'atnd_time', 'status']

    class Meta:
        model = AttendanceRaw


class AttendanceDetailAdmin(admin.ModelAdmin):
    list_display = ['emp_no', 'att_date']

    class Meta:
        model = AttendanceDetail


admin.site.register(AccountBank, AccountBankAdmin)
admin.site.register(AttendanceRaw, AttendanceRawAdmin)
admin.site.register(AttendanceDetail, AttendanceDetailAdmin)
