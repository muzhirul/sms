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

class SectionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Section Information",{'fields':[('code','section','institution','status'),]})
    ]
    list_display = ['code','section','institution','status','created_at']
    search_fields = ['code','section','institution']
    save_on_top = True
    list_per_page = 15

class ClassAdmin(admin.ModelAdmin):
    list_display = ['code','name','institution']
    search_fields = ['code','name','institution']
    filter_horizontal = ('section',)
    save_on_top = True
    list_per_page = 15

    class Meta:
        model = Class

admin.site.register(Session,SessionAdmin)
admin.site.register(Section,SectionAdmin)
admin.site.register(Class,ClassAdmin)