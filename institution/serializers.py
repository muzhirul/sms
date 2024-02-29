from rest_framework import serializers
from .models import *


class InstitutionViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Institution
        fields = ['id','name','mobile_no','email','logo']

class BranchViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = ['id','name','mobile_no','email']