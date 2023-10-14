from rest_framework import serializers
from .models import *

class GradeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Grade
        fields = ['id','name','start_mark','end_mark','point','sl_no']