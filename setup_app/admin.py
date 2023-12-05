from django.contrib import admin
from .models import *
# Register your models here.


class SetupAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Basic Information", {'fields': [
         ('parent', 'type', 'title'), ('start_date', 'end_date', 'status'),]}),
    ]
    list_display = ['parent', 'type', 'title',
                    'start_date', 'end_date', 'status']
    search_fields = ['parent', 'type', 'title',
                     'start_date', 'end_date', 'status']
    list_filter = ['parent']

    # save_as = True
    save_on_top = True
    list_per_page = 15

    class Meta:
        model = Setup


class ReligionAdmin(admin.ModelAdmin):
    list_display = ['name', 'sl_no', 'created_by', 'updated_at']
    search_fields = ['name']


class GenderAdmin(admin.ModelAdmin):
    list_display = ['name', 'sl_no', 'created_by', 'updated_at']
    search_fields = ['name']


class BloodGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'sl_no', 'created_by', 'updated_at']
    search_fields = ['name']


class OccupationAdmin(admin.ModelAdmin):
    list_display = ['name', 'sl_no', 'created_by', 'updated_at']
    search_fields = ['name']


class RelationAdmin(admin.ModelAdmin):
    list_display = ['name', 'sl_no', 'created_by', 'updated_at']
    search_fields = ['name']


class MenuAdmin(admin.ModelAdmin):
    list_display = ['parent', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'slug']

    class Meta:
        model = Menu


class PermissionAdmin(admin.ModelAdmin):
    list_display = ['role', 'menu', 'can_create',
                    'can_view', 'can_update', 'can_delete', 'status']
    list_editable = ['can_create', 'can_view', 'can_update', 'can_delete']

    class Meta:
        model = Permission


class PermissionTabularAdmin(admin.TabularInline):

    # list_editable = ['can_create','can_view','can_update','can_delete']
    model = Permission
    fields = ['menu', 'can_create', 'can_view',
              'can_update', 'can_delete', 'status']
    extra = 0


class RoleAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Role Information", {'fields': [('name', 'status'),]})
    ]
    list_display = ['name', 'status', 'created_at']

    class Meta:
        model = Role
    inlines = [PermissionTabularAdmin]


class DayAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'long_name','week_end','created_by', 'created_at']

    class Meta:
        model = Days


class FloorTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'sl_no', 'status', 'created_at']

    class Meta:
        model = FloorType


class SubjectTypeAdmin(admin.ModelAdmin):
    fields = ['name', 'status']

    class Meta:
        model = SubjectType


class EducationBoardAdmin(admin.ModelAdmin):
    list_display = ['board_code', 'name', 'status']

    class Meta:
        model = EducationBoard


class DivisionAdmin(admin.ModelAdmin):
    list_display = ['divi_code', 'name', 'country', 'status']

    class Meta:
        model = Division


class DistrictAdmin(admin.ModelAdmin):
    list_display = ['dist_code', 'name', 'division', 'status']

    class Meta:
        model = District


class CountryAdmin(admin.ModelAdmin):
    list_display = ['coun_code', 'name', 'status']

    class Meta:
        model = Country


class ThanaAdmin(admin.ModelAdmin):
    list_display = ['thana_code', 'name', 'district', 'status']

    class Meta:
        model = Thana


class ContractTypeAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'status']

    class Meta:
        model = ContractType

class MaritalStatusAdmin(admin.ModelAdmin):
    list_display = ['name','status']

    class Meta:
        model = MaritalStatus
        


admin.site.register(Setup, SetupAdmin)
admin.site.register(Gender, GenderAdmin)
admin.site.register(Religion, ReligionAdmin)
admin.site.register(BloodGroup, BloodGroupAdmin)
admin.site.register(Occupation, OccupationAdmin)
admin.site.register(Relation, RelationAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Days, DayAdmin)
admin.site.register(FloorType, FloorTypeAdmin)
admin.site.register(SubjectType, SubjectTypeAdmin)
admin.site.register(EducationBoard, EducationBoardAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Thana, ThanaAdmin)
admin.site.register(ContractType, ContractTypeAdmin)
admin.site.register(MaritalStatus, MaritalStatusAdmin)
