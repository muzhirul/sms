from rest_framework import serializers
from setup_app.serializers import *
from hrms.serializers import AccountBankViewSerializer
from staff.models import *
from academic.models import *
from hrms.serializers import *


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

class StaffShiftListSerializer2(serializers.ModelSerializer):
    class Meta:
        model = StaffShift
        fields = ['id','name']

class EducationViewSerializer(serializers.ModelSerializer):
    edu_board = EducationBoardViewSerializer(read_only=True)
    class Meta:
        model = Education
        exclude = ['staff','institution','branch','status','created_at','updated_at','created_by','updated_by']

    def to_representation(self, instance):
        if instance.status:
            return super().to_representation(instance)
        else:
            return None
     
class EducationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)        
    class Meta:
        model = Education
        # fields = '__all__'
        exclude = ['status','created_at','updated_at','created_by','updated_by']

class StaffPayrollViewSerializer(serializers.ModelSerializer):
    contract_type = ContractTypeViewSerializer(read_only=True)
    class Meta:
        model = StaffPayroll
        exclude = ['staff','status','created_at','updated_at','created_by','updated_by','institution','branch']

    def to_representation(self, instance):
        if instance.status:
            return super().to_representation(instance)
        else:
            return None

class StaffPayrollCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = StaffPayroll
        exclude = ['status','created_at','updated_at','created_by','updated_by','institution','branch']

class StaffBankViewSerializer(serializers.ModelSerializer):
    bank_name = AccountBankViewSerializer(read_only=True)
    class Meta:
        model = StaffBankAccountDetails
        exclude = ['staff','status','created_at','updated_at','created_by','updated_by','institution','branch']

    def to_representation(self, instance):
        if instance.status:
            return super().to_representation(instance)
        else:
            return None

class StaffBankCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
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
        else:
            return None      

class StaffSocialMediaCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = StaffSocialMedia
        exclude = ['status','created_at','updated_at','created_by','updated_by','institution','branch']

class ProcessAttendanceViewDailySerializer(serializers.ModelSerializer):
    shift = StaffShiftListSerializer2()
    attn_type = AttendanceTypeViewSerializer()
    class Meta:
        model = ProcessAttendanceDaily
        # exclude = ['role','process_date','staff','staff_code','con_type','institution','branch','status','created_at','updated_at','created_by','updated_by']
        fields = ['attn_date','shift','get_day_name','attn_type','in_time','out_time','duration']

class StaffLeaveViewSerialier(serializers.ModelSerializer):
    leave_type = LeaveTypeView2Serializer()
    class Meta:
        model = StaffLeave
        fields = ['leave_type','leave_days','taken_days','is_active']

class StaffLeaveListSerialier(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    leave_type_code = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = StaffLeave
        fields = ['id', 'leave_type_code', 'name']

    def get_id(self, obj):
        return obj.leave_type.id

    def get_leave_type_code(self, obj):
        return obj.leave_type.leave_type_code

    def get_name(self, obj):
        return obj.leave_type.name
        
class StaffTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id','first_name','last_name','mobile_no','staff_id','user']
        
class StaffTeacherWithSubjectSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()
    class Meta:
        model = Staff
        fields = ['id','first_name','last_name','mobile_no','staff_id', 'subjects']
    
    def get_subjects(self, obj):
        # Assuming `obj` is an instance of `Staff`
        institution = self.context['request'].user.institution
        branch = self.context['request'].user.branch
        
        # Find all routine details related to this teacher
        routine_details = ClassRoutiineDtl.objects.filter(
            teacher=obj,
            status=True,
            institution=institution,
            branch=branch
        ).select_related('class_subject')

        # Return a list of subjects taught by the teacher
        return [
            {
                "subject_id": rd.class_subject.id,
                "subject_name": rd.class_subject.subject.name
            }
            for rd in routine_details if rd.class_subject
        ]


class StaffTeacherViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = ['id','name','staff_id','mobile_no']
        
    def to_representation(self, instance):
        if instance.status:
            return super().to_representation(instance)
        else:
            return None

class StaffLeaveAppHistoryViewSerializer(serializers.ModelSerializer):
    approve_group = SetupViewSerializer(read_only=True)
    approve_by = StaffTeacherViewSerializer(read_only=True)
    app_status = SetupViewSerializer(read_only=True)
    class Meta:
        model = StaffLeaveAppHistory
        exclude = ['status','is_active','leave_trns','created_at','updated_at','created_by','updated_by','institution','branch']

class StaffLeaveAppHistoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaffLeaveAppHistory
        fields = ['app_status','remarks','approve_date']

class StaffLeaveAppHistoryViewSerializer(serializers.ModelSerializer):
    approve_group = SetupViewSerializer(read_only=True)
    approve_by = StaffTeacherViewSerializer(read_only=True)
    app_status = SetupViewSerializer(read_only=True)
    class Meta:
        model = StaffLeaveAppHistory
        exclude = ['status','is_active','leave_trns','created_at','updated_at','created_by','updated_by','institution','branch']

class StaffLeaveTransactionListSerializer(serializers.ModelSerializer):
    leave_type = LeaveTypeView2Serializer(read_only=True)
    apply_by = StaffTeacherViewSerializer(read_only=True)
    app_status = SetupViewSerializer(read_only=True)
    responsible = StaffTeacherViewSerializer(read_only=True)
    approval_path = StaffLeaveAppHistoryViewSerializer(read_only=True,many=True)

    class Meta:
        model = StaffLeaveTransaction
        exclude = ['status']

class StaffLeaveTransactionViewSerializer(serializers.ModelSerializer):
    leave_type = LeaveTypeView2Serializer(read_only=True)
    apply_by = StaffTeacherViewSerializer(read_only=True)
    app_status = SetupViewSerializer(read_only=True)
    responsible = StaffTeacherViewSerializer(read_only=True)

    class Meta:
        model = StaffLeaveTransaction
        exclude = ['status']

class AttendanceDailyCreateRawSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttendanceDailyRaw
        exclude = ['status','created_by','updated_by','created_at','updated_at']

    def to_representation(self, instance):
        if instance.status:
            return super().to_representation(instance)
        else:
            return None

class AttendanceDailyRawViewSerializer(serializers.ModelSerializer):
    staff = StaffTeacherViewSerializer(read_only=True)
    class Meta:
        model = AttendanceDailyRaw
        exclude = ['status','institution','branch','created_by','updated_by','created_at','updated_at']
    
    def to_representation(self, instance):
        if instance.status:
            return super().to_representation(instance)
        else:
            return None

class staffCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        # fields = ['first_nmae','last_name']
        exclude = ['code','user','institution','branch','status']

class staffSerializer(serializers.ModelSerializer):
    staff_education = EducationSerializer(many=True)
    payroll = StaffPayrollCreateSerializer(many=True)
    bank_info = StaffBankCreateSerializer(many=True)
    social_media = StaffSocialMediaCreateSerializer(many=True)

    class Meta:
        model = Staff
        # fields = ['first_nmae','last_name']
        exclude = ['code','user','institution','branch','status']

    def update(self, instance, validated_data):
        staff_payrolls = validated_data.pop('payroll', [])
        staff_educations = validated_data.pop('staff_education',[])
        social_medias = validated_data.pop('social_media',[])
        bank_infos = validated_data.pop('bank_info',[])
        for key, value in validated_data.items():
            setattr(instance, key, value)
        # instance.step = validated_data.get("step", instance.step)
        # instance.first_name = validated_data.get("first_name", instance.first_name)
        # instance.last_name = validated_data.get("last_name", instance.last_name)
        # instance.gender = validated_data.get("gender", instance.gender)
        # instance.dob = validated_data.get("dob", instance.dob)
        # instance.mobile_no = validated_data.get("mobile_no", instance.mobile_no)
        # instance.emergency_number = validated_data.get("emergency_number", instance.emergency_number)
        # instance.nid = validated_data.get("nid", instance.nid)
        # instance.religion = validated_data.get("religion", instance.religion)
        # instance.email = validated_data.get("email", instance.email)
        # instance.blood_group = validated_data.get("blood_group", instance.blood_group)
        # instance.marital_status = validated_data.get("marital_status", instance.marital_status)
        # instance.present_address = validated_data.get("present_address", instance.present_address)
        # instance.permanent_address = validated_data.get("permanent_address", instance.permanent_address)
        # instance.doj = validated_data.get("doj", instance.doj)
        # instance.designation = validated_data.get("designation", instance.designation)
        # instance.department = validated_data.get("department", instance.department)
        # instance.shift = validated_data.get("shift", instance.shift)
        instance.save()
        keep_socials = []
        kepp_banks_id = []
        keep_edu_id = []
        keep_payroll_id = []
        try:
            for staff_payroll in staff_payrolls:
                if "id" in staff_payroll.keys():
                    if StaffPayroll.objects.filter(id=staff_payroll["id"]).exists():
                        p = StaffPayroll.objects.get(id=staff_payroll["id"])
                        p.order_seq = staff_payroll.get('order_seq',p.order_seq)
                        p.gross = staff_payroll.get('gross',p.gross)
                        p.basic = staff_payroll.get('basic',p.basic)
                        p.medical = staff_payroll.get('medical',p.medical)
                        p.convence = staff_payroll.get('convence',p.convence)
                        p.others = staff_payroll.get('others',p.others)
                        p.start_date = staff_payroll.get('start_date',p.start_date)
                        p.end_date = staff_payroll.get('end_date',p.end_date)
                        p.remarks = staff_payroll.get('remarks',p.remarks)
                        p.contract_type = staff_payroll.get('contract_type',p.contract_type)
                        p.is_active = staff_payroll.get('is_active',p.is_active)
                        p.status = True
                        p.save()
                        keep_payroll_id.append(p.id)
                    else:
                        continue
                else:
                    p = StaffPayroll.objects.create(**staff_payroll,staff=instance,institution=instance.institution,branch=instance.branch)
                    keep_payroll_id.append(p.id)
                    
                for payroll in StaffPayroll.objects.filter(staff=instance):
                    if payroll.id not in keep_payroll_id:
                        payroll.status = False
                        payroll.save()
        except:
            pass
        try:
            for staff_education in staff_educations:
                if "id" in staff_education.keys():
                    if Education.objects.filter(id=staff_education["id"]).exists():
                        e = Education.objects.get(id=staff_education["id"])
                        e.order_seq = staff_education.get('order_seq', e.order_seq)
                        e.edu_board = staff_education.get('edu_board', e.edu_board)
                        e.institution_name = staff_education.get('institution_name', e.institution_name)
                        e.registration_no = staff_education.get('registration_no', e.registration_no)
                        e.title = staff_education.get('title', e.title)
                        e.start_date = staff_education.get('start_date', e.start_date)
                        e.end_date = staff_education.get('end_date', e.end_date)
                        e.passing_year = staff_education.get('passing_year', e.passing_year)
                        e.result = staff_education.get('result', e.result)
                        e.result_out_of = staff_education.get('result_out_of', e.result_out_of)
                        e.remarks = staff_education.get('remarks', e.remarks)
                        e.status = True
                        e.save()
                        keep_edu_id.append(e.id)
                    else:
                        continue
                else:
                    e = Education.objects.create(**staff_education,staff=instance,institution=instance.institution,branch=instance.branch)
                    keep_edu_id.append(e.id)

                for education in instance.staff_education.all():
                    if education.id not in keep_edu_id:
                        education.status = False
                        education.save()
        except:
            pass

        try:
            for bank_info in bank_infos:
                if "id" in bank_info.keys():
                    if StaffBankAccountDetails.objects.filter(id=bank_info["id"]).exists():
                        b = StaffBankAccountDetails.objects.get(id=bank_info["id"])
                        b.bank_name = bank_info.get('bank_name', b.bank_name)
                        b.account_title = bank_info.get('account_title', b.account_title)
                        b.account_number = bank_info.get('account_number', b.account_number)
                        b.branch_name = bank_info.get('branch_name', b.branch_name)
                        b.remarks = bank_info.get('remarks', b.remarks)
                        b.is_active = bank_info.get('is_active', b.is_active)
                        b.status = True
                        b.save()
                        kepp_banks_id.append(b.id)
                    else:
                        continue
                else:
                    b = StaffBankAccountDetails.objects.create(**bank_info,staff=instance,institution=instance.institution,branch=instance.branch)
                    kepp_banks_id.append(b.id)

            for bank in instance.bank_infos.all():
                if bank.id not in kepp_banks_id:
                    bank.status = False
                    bank.save()
        except:
            pass

        try:
            for social_media in social_medias:
                if "id" in social_media.keys():
                    if StaffSocialMedia.objects.filter(id=social_media["id"]).exists():
                        a = StaffSocialMedia.objects.get(id=social_media["id"])
                        a.name = social_media.get('name', a.name)
                        a.username = social_media.get('username', a.username)
                        a.url = social_media.get('url', a.url)
                        a.status = True
                        a.save()
                        keep_socials.append(a.id)
                    else:
                        continue
                else:
                    s = StaffSocialMedia.objects.create(**social_media, staff=instance,institution=instance.institution,branch=instance.branch)
                    keep_socials.append(s.id)
            
            for media in instance.social_medias.all():
                if media.id not in keep_socials:
                    media.status = False
                    media.save()
        except:
            pass
        return instance
        
class staffSerializer2(serializers.ModelSerializer):
    gender = GenderSerializer(read_only=True)
    religion = ReligionSerializer(read_only=True)
    blood_group = BloodGroupSerializer(read_only=True)
    designation = DesignationListSerializer(read_only=True)
    department = DepartmentListSerializer(read_only=True)
    shift = StaffShiftListSerializer2(read_only=True)
    role = RoleSerializer(read_only=True)
    marital_status = MaritalStatusViewSerializer(read_only=True)
    staff_education = EducationViewSerializer(many=True, required=False, read_only=True)
    payroll =StaffPayrollViewSerializer(many=True, required=False, read_only=True)
    bank_info = StaffBankViewSerializer(many=True, required=False, read_only=True)
    social_media = StaffSocialMediaViewSerializer(many=True, required=False, read_only=True)
    atten_daily = ProcessAttendanceViewDailySerializer(many=True, required=False, read_only=True)
    staff_leave = StaffLeaveViewSerialier(many=True, required=False, read_only=True)
    staff_leave_trns = StaffLeaveTransactionViewSerializer(many=True, required=False, read_only=True)
    # shift = StaffShiftListCreate(read_only=True)
    class Meta:
        model = Staff
        # fields = ['first_nmae','last_name']
        exclude = ['code','last_attn_proc_date','user','institution','branch','status']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Filter out None values from the social_media list 
        representation['staff_education'] = [item for item in representation['staff_education'] if item is not None]
        representation['payroll'] = [item for item in representation['payroll'] if item is not None]
        representation['bank_info'] = [item for item in representation['bank_info'] if item is not None]
        representation['social_media'] = [item for item in representation['social_media'] if item is not None]
        # Order std_atten_daily by attn_date
        representation['atten_daily'] = sorted(
            representation['atten_daily'],
            key=lambda x: x['attn_date'],
            reverse=True
        )

        if not instance.status:
            # If status is False, exclude the social_media field
            representation.pop('staff_education', None)
            representation.pop('payroll', None)
            representation.pop('bank_info', None)
            representation.pop('social_media', None)

        return representation
     
class StaffShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffShift
        exclude = ['status','code','start_date','end_date','start_buf_min','end_buf_min','institution','branch']

class StaffLeaveCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffLeave
        exclude = ['status']

class StaffLeaveTransactionCreateSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    class Meta:
        model = StaffLeaveTransaction
        exclude = ['updated_at','created_at','status','day_count','tran_type','application_date','app_status','active_start_date','active_end_date','is_active','institution','branch','created_by','updated_by']

class ProcessStaffAttendanceMstCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessStaffAttendanceMst
        exclude = ['updated_at','created_at','code','total_day','created_by','updated_by']

class StaffStatusTransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffStatusTransaction
        exclude = ['updated_at','created_at','status','is_active','created_by','updated_by']

class StaffStatusTransactionViewSerializer(serializers.ModelSerializer):
    staff = StaffTeacherSerializer(read_only=True)
    staff_status = ActiveStatusViewSerializer(read_only=True)
    class Meta:
        model = StaffStatusTransaction
        fields = ['id','code','staff','staff_status','start_date','end_date','reason','remarks']
