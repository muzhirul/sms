from django.contrib import admin
from .models import *
# Register your models here.

class AccountBankAdmin(admin.ModelAdmin):
    list_display = ['name','status']
    
    class Meta:
        model = AccountBank
        
admin.site.register(AccountBank,AccountBankAdmin)