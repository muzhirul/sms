from rest_framework import serializers
from .models import *
from academic.serializers import *

class GradeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Grade
        fields = ['id','name','start_mark','end_mark','point','sl_no']
        
class ExamNameCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExamName
        exclude = ['status','created_by','updated_by','created_at','updated_at']

class ExamNameViewSerializer(serializers.ModelSerializer):
    session = SessionSerializer2(read_only=True)
    class Meta:
        model = ExamName
        fields = ['id','name','session','sl_no']

class ExamNameListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamName
        fields = ['id','name']
        
# class ExamRoutineSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = ExamRoutine
#         exclude = ['status','institution','branch','created_by','updated_by','created_at','updated_at']
        
class ExamRoutineDtlViewSerializers(serializers.ModelSerializer):
    teacher = StaffTeacherViewSerializer(read_only=True,many=True)
    subject = SubjectViewSerializer(read_only=True)
    room = ClassRoomSerializer2(read_only=True)
    class Meta:
        model = ExamRoutineDtl
        fields = ['id','day','subject','room','exam_date','start_time','end_time','duration','teacher']

    def to_representation(self, instance):
        if instance.status:
            return super().to_representation(instance)
        else:
            return None
        
class ExamRoutineMstViewSerializers(serializers.ModelSerializer):
    exam = ExamNameListSerializer(read_only=True)
    version = VersionSerializer2(read_only=True)
    session = SessionSerializer2(read_only=True)
    class_name = ClassSerializer2(read_only=True)
    section = SectionSerializer2(read_only=True)
    group = ClassGroupListSerializer(read_only=True)
    exam_routine_dtl = ExamRoutineDtlViewSerializers(many=True, required=False, read_only=True)

    class Meta:
        model = ExamRoutineMst
        exclude = ['institution','branch','status','created_at','updated_at','created_by','updated_by']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Filter out None values from the social_media list 
        representation['exam_routine_dtl'] = [item for item in representation['exam_routine_dtl'] if item is not None]

        if not instance.status:
            # If status is False, exclude the social_media field
            representation.pop('exam_routine_dtl', None)

        return representation
    
class ExamRoutineDtlCreateSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = ExamRoutineDtl
        exclude = ['institution','branch','status','created_at','updated_at','created_by','updated_by']
        read_only_fields = ('exam_routine_mst',)
    
class ExamRoutineMstCreateSerializers(serializers.ModelSerializer):
    exam_routine_dtl = ExamRoutineDtlCreateSerializers(many=True)
    class Meta:
        model = ExamRoutineMst
        exclude = ['institution','branch','status','created_at','updated_at','created_by','updated_by']

    def create(self,validated_data):
        routine_dtls = validated_data.pop('exam_routine_dtl')
        routine_mst = ExamRoutineMst.objects.create(**validated_data)
        for routine_dtl in routine_dtls:
            teachers_data = routine_dtl.pop('teacher', [])  # Extract teacher data
            exam_del = ExamRoutineDtl.objects.create(**routine_dtl, exam_routine_mst=routine_mst,institution=routine_mst.institution,branch=routine_mst.branch)
            exam_del.teacher.set(teachers_data)
        return routine_mst