from rest_framework import serializers
from .models import *


class InstitutionViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Institution
        fields = ['name','mobile_no','email','address','logo']

class BranchViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = ['name','mobile_no','address','email']