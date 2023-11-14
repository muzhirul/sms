from rest_framework import serializers
from .models import *
from setup_app.serializers import BloodGroupSerializer, GenderSerializer, ReligionSerializer, OccupationSerializer, RelationSerializer
from academic.serializers import VersionSerializer2, SessionSerializer2, ClassSerializer2,SectionSerializer2

class StudentEnrollViewSerializer(serializers.ModelSerializer):
    version = VersionSerializer2(read_only=True)
    session = SessionSerializer2(read_only=True)
    class_name = ClassSerializer2(read_only=True)
    section = SectionSerializer2(read_only=True)
    class Meta:
        model = StudentEnroll
        exclude = ['student','institution','branch','status','created_by', 'updated_by', 'created_at', 'updated_at']

class StudentEnrollSerialize(serializers.ModelSerializer):
    class Meta:
        model = StudentEnroll
        exclude = ['status','created_by', 'updated_by', 'created_at', 'updated_at']

class GuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        # Exclude the 'status' field and other fields you want to exclude
        exclude = ['status','created_by', 'updated_by', 'created_at', 'updated_at']

class StudentSerializer(serializers.ModelSerializer):
    guardians = GuardianSerializer(many=True, required=False, read_only=True)
    enroll = StudentEnrollSerialize(many=True, required=False, read_only=True)
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
        exclude = ['user','student','status','created_by', 'updated_by', 'created_at', 'updated_at']
        
class StudentViewSerializer(serializers.ModelSerializer):
    guardians = GuardianViewSerializer(many=True, required=False, read_only=True)
    enroll = StudentEnrollViewSerializer(many=True, required=False, read_only=True)
    gender = GenderSerializer(read_only=True)
    religion = ReligionSerializer(read_only=True)
    blood_group = BloodGroupSerializer(read_only=True)
    class Meta:
        model = Student
        # Exclude the 'status' field and other fields you want to exclude
        exclude = ['status','user','created_by', 'updated_by', 'created_at', 'updated_at','institution','branch']
        
