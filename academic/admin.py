from django.contrib import admin
from academic.models import *

# Register your models here.
class VersionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Version Information",{'fields':[('version','status'),]})
    ]
    list_display = ['code','version','status','created_at','updated_by','updated_at']
    search_fields = ['code','version','status']
    save_on_top = True
    list_per_page = 15

    class Meta:
        model = Version
class SessionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Session Information",{'fields':[('session','status'),]})
        # ("Session Information",{'fields':[('code','session','institution','branch','status'),]})
    ]
    list_display = ['code','session','institution','branch','status','created_by','created_at']
    search_fields = ['code','session','institution']
    save_on_top = True
    list_per_page = 15

class ClassGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'status']
    fields = ['code','name','status']

    class Meta:
        model = ClassGroup

class SectionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Section Information",{'fields':[('section','status'),]})
        # ("Section Information",{'fields':[('code','section','institution','branch','status'),]})
    ]
    list_display = ['code','section','institution','branch','status','created_at']
    search_fields = ['code','section','institution']
    save_on_top = True
    list_per_page = 15

class SubjectAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Subject Information",{"fields":[('code','type','name'),]})
        # ("Subject Information",{"fields":[('code','type','institution','branch'),('name','picture','status'),('start_date','end_date'),]})
    ]
    list_display = ['code','type','name','status','created_at']
    search_fields = ['code','type','name','status']
    save_on_top = True
    list_per_page = 15

    class Meta:
        model = Subject

class ClassAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Class Information",{'fields':[('name'),]}),
        # ("Class Information",{'fields':[('code','name','section','version','session','institution','branch','status'),]}),
        # ("Subject Information",{'fields':[('subject',)]}),
        # ("Section Information",{'fields':[('section',)]}),
    ]
    list_display = ['name','status']
    search_fields = ['name']
    # filter_horizontal = ('section','subject')
    save_on_top = True
    list_per_page = 15

    class Meta:
        model = ClassName
    
class ClassRoomAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Class Room Information",{"fields":[('room_no','building','floor_type',),]})
        # ("Class Room Information",{"fields":[('code','building','location'),('start_date','end_date'),('room_no','institution','branch','status')]})
    ]
    list_display = ['building','floor_type','room_no','status']
    search_fields = ['building','floor_type','room_no','status']
    save_on_top = True
    list_per_page = 15

    class Meta:
        model = ClassRoom

class ClassPeriodAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Class Period Information",{"fields":[('name'),('start_time','end_time')]})
        # ("Class Period Information",{"fields":[('code','name'),('start_time','end_time'),('duration','status')]})
    ]
    list_display = ['name','start_time','end_time','duration','status']
    search_fields = ['name','start_time','end_time','duration']
    save_on_top = True
    list_per_page = 15

    class Meta:
        model = ClassPeriod
        
class ClassSectionAdmin(admin.ModelAdmin):
    fields = ['class_name','section','group','session','version']
    list_display = ['class_name','group','section','session','version','status']
    search_fields = ['class_name__name','section__section','session__session']
    class Meta:
        model = ClassSection
        
class ClassSubjectAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Class Subject Information",{"fields":[('class_name'),('code','subject','image','book_file'),('section','session','version')]})
    ]
    list_display = ['class_name','code','subject','section','session','version']
    search_fields = ['subject__name']
    class Meta:
        model = ClassSubject

class ClassTeacherAdmin(admin.ModelAdmin):
    list_display = ['class_name','section','group','session','version','teacher']
    class Meta:
        model = ClassTeacher

class ClassRoutineAdmin(admin.ModelAdmin):
    fields = ['teacher','class_name','section','subject','class_period','day','class_room','session','version','status']
    list_display = ['teacher','class_name','section','subject','class_period','day','class_room','session','version','status']
    
    class Meta:
        model = ClassRoutine
        
class ClassRoutineDtlAdmin(admin.TabularInline):
    model = ClassRoutiineDtl
    fields = ['teacher','subject','class_period','class_room','status']
    extra = 6
    
class ClassRoutineMstAdmin(admin.ModelAdmin):
    list_display = ['class_name','section','day','session','version','institution','branch']
    class Meta:
        model = ClassRoutineMst
        
    inlines = [ClassRoutineDtlAdmin]



admin.site.register(Version,VersionAdmin)
admin.site.register(Session,SessionAdmin)
admin.site.register(Section,SectionAdmin)
admin.site.register(ClassGroup,ClassGroupAdmin)
admin.site.register(ClassName,ClassAdmin)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(ClassRoom,ClassRoomAdmin)
admin.site.register(ClassPeriod,ClassPeriodAdmin)
admin.site.register(ClassSection,ClassSectionAdmin)
admin.site.register(ClassSubject,ClassSubjectAdmin)
admin.site.register(ClassTeacher,ClassTeacherAdmin)
admin.site.register(ClassRoutine,ClassRoutineAdmin)
admin.site.register(ClassRoutineMst, ClassRoutineMstAdmin)