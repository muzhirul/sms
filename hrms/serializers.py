from rest_framework import serializers
from hrms.models import *
from setup_app.serializers import *


class AccountBankSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    institution_name = serializers.ReadOnlyField(source='institution.name')
    branch_name = serializers.ReadOnlyField(source='branch.name')
    class Meta:
        model = AccountBank
        # Exclude the 'status' field and other fields you want to exclude
        exclude = ['status']
        # exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']

class AccountBankViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountBank
        # Exclude the 'status' field and other fields you want to exclude
        fields = ['id','name']
        # exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']

class HolidaySerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = Holiday
        exclude = ['status']

class HolidayViewSerializer(serializers.ModelSerializer):
    type = HolidayTypeViewSerializer(read_only=True)
    
    class Meta:
        model = Holiday
        exclude = ['status','institution','branch','created_by','updated_by','created_at','updated_at']

class LeaveTypeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeaveType
        exclude = ['status','institution','branch']

class LeaveTypeListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LeaveType
        fields = ['id','leave_type_code','name']

class LeaveTypeViewSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = LeaveType
        exclude = ['status','institution','branch']

class LeaveTypeView2Serializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = ['id','leave_type_code','name']
        # exclude = ['status','institution','branch']

class PayrollElementViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollElement
        fields = ['id','name']

class SalarySetupDtlViewSerializer(serializers.ModelSerializer):
    payroll_ele = PayrollElementViewSerializer()
    class Meta:
        model = SalarySetupDtl
        fields = ['id', 'payroll_ele','fixed_amt','formula','min_amt','max_amt','remarks','status']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Original formula string
        formula = representation.get('formula', '')

        # Fetch all mappings from the PayrollElement table
        formula_mapping = {
            element.value: element.name
            for element in PayrollElement.objects.all()
        }

        # Build the formula as a list of key-value pairs
        formula_parts = formula.split()
        formula_list = []
        
        for part in formula_parts:
            if part in formula_mapping:
                # Add the formula part as a key-value pair
                formula_list.append({part: formula_mapping[part]})
            # elif part == '*':
            #     formula_list.append({part: "Multiply"})
            # elif part.replace('.', '', 1).isdigit():
            #     percentage = f"{float(part) * 100:.0f}%"
            #     formula_list.append({part: percentage})

        # Replace the formula representation with the new list format
        representation['formula'] = formula_list

        return representation

class SalarySetupMstViewSerializer(serializers.ModelSerializer):
    salary_setup_dtl = SalarySetupDtlViewSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = SalarySetupMst
        fields = ['id','code','name','status','salary_setup_dtl']


