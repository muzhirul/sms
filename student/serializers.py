from rest_framework import serializers
from .models import *
from setup_app.serializers import *
from staff.serializers import StaffShiftListSerializer2
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

class StudentSortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id','student_no','first_name','last_name']

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

class ProcessStAttendanceDailyViewDailySerializer(serializers.ModelSerializer):
    shift = StaffShiftListSerializer2()
    attn_type = AttendanceTypeViewSerializer()
    class Meta:
        model = ProcessStAttendanceDaily
        # exclude = ['role','process_date','staff','staff_code','con_type','institution','branch','status','created_at','updated_at','created_by','updated_by']
        fields = ['attn_date','shift','get_day_name','attn_type','in_time','out_time','duration']

class ProcessStAttendanceDailySearchDailySerializer(serializers.ModelSerializer):
    student = StudentSortViewSerializer()
    attn_type = AttendanceTypeViewSerializer()
    class Meta:
        model = ProcessStAttendanceDaily
        fields = ['id','roll','attn_date','student','attn_type']

        
class StudentViewSerializer(serializers.ModelSerializer):
    guardians = GuardianViewSerializer(many=True, required=False, read_only=True)
    enroll = StudentEnrollViewSerializer(many=True, required=False, read_only=True)
    std_atten_daily = ProcessStAttendanceDailyViewDailySerializer(many=True, required=False, read_only=True)
    gender = GenderSerializer(read_only=True)
    religion = ReligionSerializer(read_only=True)
    blood_group = BloodGroupSerializer(read_only=True)
    class Meta:
        model = Student
        # Exclude the 'status' field and other fields you want to exclude
        exclude = ['status','user','created_by', 'updated_by', 'created_at', 'updated_at','institution','branch']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Order std_atten_daily by attn_date
        representation['std_atten_daily'] = sorted(
            representation['std_atten_daily'],
            key=lambda x: x['attn_date'],
            reverse=True
        )

        return representation
        
