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
        fields = ['name']
        
class ReligionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Religion
        fields = ['id','name']
    
class BloodGroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BloodGroup
        fields = ['id','name']
        
class GenderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Gender
        fields = ['id','name']
        
class OccupationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Occupation
        fields = ['id','name']
        
class RelationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Relation
        fields = ['id','name']
        
class DaySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Day
        fields = ['short_name','long_name']
        

        