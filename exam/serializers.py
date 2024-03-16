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
        
# class ExamRoutineSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = ExamRoutine
#         exclude = ['status','institution','branch','created_by','updated_by','created_at','updated_at']
        
class ExamRoutineDtlViewSerializers(serializers.ModelSerializer):
    # teacher = StaffTeacherViewSerializer(read_only=True)
    subject = SubjectViewSerializer(read_only=True)
    room = ClassRoomSerializer2(read_only=True)
    class Meta:
        model = ExamRoutineDtl
        fields = ['id','day','subject','room','start_time','end_time','duration']

    # def to_representation(self, instance):
    #     if instance.status:
    #         return super().to_representation(instance)
    #     else:
    #         return None
        
class ExamRoutineMstViewSerializers(serializers.ModelSerializer):
    version = VersionSerializer2(read_only=True)
    session = SessionSerializer2(read_only=True)
    class_name = ClassSerializer2(read_only=True)
    section = SectionSerializer2(read_only=True)
    group = ClassGroupListSerializer(read_only=True)
    exam_routine_dtl = ExamRoutineDtlViewSerializers(many=True, required=False, read_only=True)

    class Meta:
        model = ExamRoutineMst
        exclude = ['institution','branch','status','created_at','updated_at','created_by','updated_by']

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)

    #     # Filter out None values from the social_media list 
    #     representation['exam_routine_dtl'] = [item for item in representation['exam_routine_dtl'] if item is not None]

    #     if not instance.status:
    #         # If status is False, exclude the social_media field
    #         representation.pop('exam_routine_dtl', None)

    #     return representation