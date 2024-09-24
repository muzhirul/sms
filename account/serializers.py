from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from .models import *

class CostofAccountSerializer(serializers.ModelSerializer):
    sub_coa = RecursiveField(many=True,required=False)

    class Meta:
        model = ChartofAccounts
        fields = ['id','coa_type','code','title','keyword','sub_coa']