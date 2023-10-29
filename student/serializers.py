from rest_framework import serializers
from .models import *
from setup_app.serializers import BloodGroupSerializer, GenderSerializer, ReligionSerializer, OccupationSerializer, RelationSerializer

class GuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        # Exclude the 'status' field and other fields you want to exclude
        exclude = ['status','created_by', 'updated_by', 'created_at', 'updated_at']

class StudentSerializer(serializers.ModelSerializer):
    guardians = GuardianSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Student
        # Exclude the 'status' field and other fields you want to exclude
        exclude = ['status','created_by', 'updated_by', 'created_at', 'updated_at']
        
class GuardianViewSerializer(serializers.ModelSerializer):
    gender = GenderSerializer(read_only=True)
    occupation = OccupationSerializer(read_only=True)
    relation = RelationSerializer(read_only=True)
    class Meta:
        model = Guardian
        # Exclude the 'status' field and other fields you want to exclude
        exclude = ['status','created_by', 'updated_by', 'created_at', 'updated_at']
        
class StudentViewSerializer(serializers.ModelSerializer):
    guardians = GuardianViewSerializer(many=True, required=False, read_only=True)
    gender = GenderSerializer(read_only=True)
    religion = ReligionSerializer(read_only=True)
    blood_group = BloodGroupSerializer(read_only=True)
    class Meta:
        model = Student
        # Exclude the 'status' field and other fields you want to exclude
        exclude = ['status','created_by', 'updated_by', 'created_at', 'updated_at','institution','branch']
        
