from django.contrib import admin
import admin_thumbnails
from institution.models import *

# Register your models here.
@admin_thumbnails.thumbnail('logo')
class InstitutionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Basic Information",{'fields':[('parent','code','name','mobile_no'),('email','logo','site_link','map_link'),]}),
        ("Address",{'fields':[('short_address','address'),]})        
    ]
    list_display = ['code','name','mobile_no','email','logo_thumbnail','status']
    search_fields = ['code','name','mobile_no','email','logo_thumbnail','status']
    # list_filter = ['blood_group']

    # save_as = True
    save_on_top = True
    list_per_page = 15

    model=Institution

admin.site.register(Institution,InstitutionAdmin)