from rest_framework import serializers
from setup_app.serializers import BloodGroupSerializer, GenderSerializer, ReligionSerializer,EducationBoardViewSerializer, ContractTypeViewSerializer,MaritalStatusViewSerializer
from hrms.serializers import AccountBankViewSerializer
from staff.models import *

class DepartmentSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    institution_name = serializers.ReadOnlyField(source='institution.name')
    branch_name = serializers.ReadOnlyField(source='branch.name')
    class Meta:
        model = Department
        # Exclude the 'status' field and other fields you want to exclude
        exclude = ['status','code']
        # exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']

class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id','name']
        
class DesignationSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    institution_name = serializers.ReadOnlyField(source='institution.name')
    branch_name = serializers.ReadOnlyField(source='branch.name')
    class Meta:
        model = Designation
        # Exclude the 'status' field and other fields you want to exclude
        exclude = ['status','code']
        # exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']

class DesignationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ['id','name']

class EducationViewSerializer(serializers.ModelSerializer):
    edu_board = EducationBoardViewSerializer(read_only=True)
    class Meta:
        model = Education
        exclude = ['staff','institution','branch','status','created_at','updated_at','created_by','updated_by']
    
    
class EducationSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Education
        # fields = '__all__'
        exclude = ['status','created_at','updated_at','created_by','updated_by']


class StaffPayrollViewSerializer(serializers.ModelSerializer):
    contract_type = ContractTypeViewSerializer(read_only=True)
    class Meta:
        model = StaffPayroll
        exclude = ['staff','status','created_at','updated_at','created_by','updated_by','institution','branch']

class StaffPayrollCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffPayroll
        exclude = ['status','created_at','updated_at','created_by','updated_by','institution','branch']

class StaffBankViewSerializer(serializers.ModelSerializer):
    bank_name = AccountBankViewSerializer(read_only=True)
    class Meta:
        model = StaffBankAccountDetails
        exclude = ['staff','status','created_at','updated_at','created_by','updated_by','institution','branch']

class StaffBankCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffBankAccountDetails
        exclude = ['status','created_at','updated_at','created_by','updated_by','institution','branch']
        
class StaffSocialMediaViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffSocialMedia
        exclude = ['staff','status','created_at','updated_at','created_by','updated_by','institution','branch']

    def to_representation(self, instance):

        if instance.status:
            return super().to_representation(instance)
        
    

class StaffSocialMediaCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = StaffSocialMedia
        exclude = ['status','created_at','updated_at','created_by','updated_by','institution','branch']
        
class StaffTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id','first_name','last_name','staff_id','user']

class staffSerializer(serializers.ModelSerializer):
    staff_education = EducationSerializer(many=True, required=False, read_only=True)
    payroll = StaffPayrollCreateSerializer(many=True, required=False, read_only=True)
    bank_info = StaffBankCreateSerializer(many=True, required=False, read_only=True)
    social_media = StaffSocialMediaCreateSerializer(many=True)

    class Meta:
        model = Staff
        # fields = ['first_nmae','last_name']
        exclude = ['code','user','institution','branch','status']

    def update(self, instance, validated_data):
        social_medias = validated_data.pop('social_media',[])
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.save()
        keep_socials = []
        
        for social_media in social_medias:
            if "id" in social_media.keys():
                if StaffSocialMedia.objects.filter(id=social_media["id"]).exists():
                    a = StaffSocialMedia.objects.get(id=social_media["id"])
                    a.name = social_media.get('name', a.name)
                    a.username = social_media.get('username', a.username)
                    a.url = social_media.get('url', a.url)
                    a.save()
                    keep_socials.append(a.id)
                else:
                    continue
            else:
                s = StaffSocialMedia.objects.create(**social_media, staff=instance)
                keep_socials.append(s.id)
                pass
        
        for media in instance.social_media.all():
            if media.id not in keep_socials:
                media.status = False
                media.save()
        return instance

class StaffShiftListSerializer2(serializers.ModelSerializer):
    class Meta:
        model = StaffShift
        fields = ['id','name']
        
class staffSerializer2(serializers.ModelSerializer):
    gender = GenderSerializer(read_only=True)
    religion = ReligionSerializer(read_only=True)
    blood_group = BloodGroupSerializer(read_only=True)
    designation = DesignationListSerializer(read_only=True)
    department = DepartmentListSerializer(read_only=True)
    shift = StaffShiftListSerializer2(read_only=True)
    marital_status = MaritalStatusViewSerializer(read_only=True)
    staff_education = EducationViewSerializer(many=True, required=False, read_only=True)
    payroll =StaffPayrollViewSerializer(many=True, required=False, read_only=True)
    bank_info = StaffBankViewSerializer(many=True, required=False, read_only=True)
    social_media = StaffSocialMediaViewSerializer(many=True, required=False, read_only=True)
    # shift = StaffShiftListCreate(read_only=True)
    class Meta:
        model = Staff
        # fields = ['first_nmae','last_name']
        exclude = ['code','user','institution','branch','status']

        
class StaffShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffShift
        exclude = ['status','code','start_date','end_date','start_buf_min','end_buf_min','institution','branch']

class StaffLeaveCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffLeave
        exclude = ['status']