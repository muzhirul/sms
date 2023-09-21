from rest_framework import serializers
from .models import *
from rest_framework_recursive.fields import RecursiveField

class MenuSerializer(serializers.ModelSerializer):
    sub_menu = RecursiveField(many=True,Required=False)
    
    class Meta:
        model: Menu
        fields = ['name','slug','icon','level','sl_no']
        
class RoleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model : Role
        field = ['name']