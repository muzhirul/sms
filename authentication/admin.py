from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authentication.models import *

# Register your models here.
class AuthenticationAdmin(UserAdmin):
    list_display = ('id','username','first_name','last_name','is_active')
    search_fields = ['username','first_name','last_name']
    filter_horizontal = ('groups', 'user_permissions','role')
    list_filter = ()
    fieldsets = ()
    class Meta:
        model = Authentication
    
admin.site.register(Authentication, AuthenticationAdmin)