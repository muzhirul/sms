from django.contrib import admin
from .models import *
# Register your models here.

class SetupAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Basic Information",{'fields':[('parent','type','title'),('start_date','end_date','status'),]}),        
    ]
    list_display = ['parent','type','title','start_date','end_date','status']
    search_fields = ['parent','type','title','start_date','end_date','status']
    list_filter = ['parent']

    # save_as = True
    save_on_top = True
    list_per_page = 15

    
    class Meta:
        model = Setup
        
class ReligionAdmin(admin.ModelAdmin):
    list_display = ['name','sl_no','created_by','updated_at']
    search_fields = ['name']
    
class GenderAdmin(admin.ModelAdmin):
    list_display = ['name','sl_no','created_by','updated_at']
    search_fields = ['name']

class BloodGroupAdmin(admin.ModelAdmin):
    list_display = ['name','sl_no','created_by','updated_at']
    search_fields = ['name']
    
class OccupationAdmin(admin.ModelAdmin):
    list_display = ['name','sl_no','created_by','updated_at']
    search_fields = ['name']
    
class RelationAdmin(admin.ModelAdmin):
    list_display = ['name','sl_no','created_by','updated_at']
    search_fields = ['name']

class MenuAdmin(admin.ModelAdmin):
    list_display = ['parent','name','slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name','slug']
    
    class Meta:
        model = Menu
        
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['role','menu','can_create','can_view','can_update','can_delete','status']
    list_editable = ['can_create','can_view','can_update','can_delete']
    class Meta:
        model = Permission
        
class DayAdmin(admin.ModelAdmin):
    list_display = ['short_name','long_name','created_by','created_at']
    
    class Meta:
        model = Day
        
class FloorTypeAdmin(admin.ModelAdmin):
    list_display = ['name','sl_no','status','created_at']
    
    class Meta:
        model = FloorType

admin.site.register(Setup,SetupAdmin)
admin.site.register(Gender,GenderAdmin)
admin.site.register(Religion,ReligionAdmin)
admin.site.register(BloodGroup,BloodGroupAdmin)
admin.site.register(Occupation,OccupationAdmin)
admin.site.register(Relation,RelationAdmin)
admin.site.register(Menu,MenuAdmin)
admin.site.register(Role)
admin.site.register(Permission,PermissionAdmin)
admin.site.register(Day,DayAdmin)
admin.site.register(FloorType,FloorTypeAdmin)
