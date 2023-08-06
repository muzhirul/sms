from django.contrib import admin
from academic.models import *

# Register your models here.
class VersionAdmin(admin.ModelAdmin):
    list_display = ['code','version','status','created_at']
    search_fields = ['code','version','status']
    save_on_top = True
    list_per_page = 15

    class Meta:
        model = Version
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

class SubjectAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Subject Information",{"fields":[('code','type','institution'),('name','picture','status'),('start_date','end_date'),]})
    ]
    list_display = ['code','type','name','status','created_at']
    search_fields = ['code','type','name','status']
    save_on_top = True
    list_per_page = 15

    class Meta:
        model = Subject

class ClassAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Class Information",{'fields':[('code','name','institution','status'),]}),
        # ("Subject Information",{'fields':[('subject',)]}),
        # ("Section Information",{'fields':[('section',)]}),
    ]
    list_display = ['code','name','institution']
    search_fields = ['code','name','institution']
    # filter_horizontal = ('section','subject')
    save_on_top = True
    list_per_page = 15

    class Meta:
        model = Class
    
class ClassRoomAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Class Room Information",{"fields":[('code','building','location'),('start_date','end_date'),('room_no','institution','status')]})
    ]
    list_display = ['code','building','location','room_no','status']
    search_fields = ['code','building','location','room_no','status']
    save_on_top = True
    list_per_page = 15

    class Meta:
        model = ClassRoom

class ClassPeriodAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Class Period Information",{"fields":[('code','name'),('start_time','end_time'),('duration','status')]})
    ]
    list_display = ['code','name','start_time','end_time','duration','status']
    search_fields = ['code','name','start_time','end_time','duration']
    save_on_top = True
    list_per_page = 15

    class Meta:
        model = ClassPeriod

admin.site.register(Version,VersionAdmin)
admin.site.register(Session,SessionAdmin)
admin.site.register(Section,SectionAdmin)
admin.site.register(Class,ClassAdmin)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(ClassRoom,ClassRoomAdmin)
admin.site.register(ClassPeriod,ClassPeriodAdmin)
admin.site.register(ClassSection)