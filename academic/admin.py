from django.contrib import admin
from academic.models import *

# Register your models here.
class SessionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Session Information",{'fields':[('code','session','institution','status'),]})
    ]
    list_display = ['code','session','institution','status','created_at']
    search_fields = ['code','session','institution']
    save_on_top = True
    list_per_page = 15

admin.site.register(Session,SessionAdmin)