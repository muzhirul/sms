from rest_framework import serializers
from .models import *

class GradeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Grade
        fields = ['id','name','start_mark','end_mark','point','sl_no']
        
class ExamNameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExamName
        exclude = ['status','institution','branch','created_by','updated_by','created_at','updated_at']
        
class ExamRoutineSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExamRoutine
        exclude = ['status','institution','branch','created_by','updated_by','created_at','updated_at']