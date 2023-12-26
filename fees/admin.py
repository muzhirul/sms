from django.contrib import admin
from .models import *

# Register your models here.

class FeesTypeAdmin(admin.ModelAdmin):
    list_display = ['name','code','is_active']
    prepopulated_fields = {'code': ('name',)}
    class Meta:
        model = FeesType

admin.site.register(FeesType, FeesTypeAdmin)