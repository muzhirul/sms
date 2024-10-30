from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from .models import *
from hrms.serializers import AccountBankViewSerializer

class CostofAccountSerializer(serializers.ModelSerializer):
    sub_coa = RecursiveField(many=True,required=False)

    class Meta:
        model = ChartofAccounts
        fields = ['id','coa_type','code','title','keyword','sub_coa']

class ChartOfAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartofAccounts
        fields = ['id', 'title', 'code','parent']

class ChartOfAccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartofAccounts
        exclude = ['created_by', 'updated_by','status','institution','branch']

class ChartOfAccountViewSerializer(serializers.ModelSerializer):
    parent = ChartOfAccountSerializer(read_only=True)
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = ChartofAccounts
        exclude = ['created_by', 'updated_by','status','institution','branch']

class ChartOfAccountSortSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = ChartofAccounts
        fields = ['id', 'title', 'code']

    def get_title(self, obj):
        title_parts = []
        current = obj
        while current is not None:
            title_parts.insert(0, current.title)
            current = current.parent
        return " > ".join(title_parts)

class CostofAccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartofAccounts
        fields = ['id','coa_type','code','title']

class AccLedgerViewSerializer(serializers.ModelSerializer):
    acc_coa = CostofAccountListSerializer(read_only=True)
    acc_coa_ref = CostofAccountListSerializer(read_only=True)

    class Meta:
        model = AccountLedger
        fields = ['gl_date','voucher_no', 'acc_coa', 'acc_coa_ref','narration','particulars', 'debit_amt', 'credit_amt'] 

class AccLedgerSerializer(serializers.ModelSerializer):
    acc_coa = CostofAccountListSerializer(read_only=True)
    acc_coa_ref = CostofAccountListSerializer(read_only=True)
    balance = serializers.SerializerMethodField()

    class Meta:
        model = AccountLedger
        fields = ['gl_date','voucher_no', 'acc_coa', 'acc_coa_ref','narration','particulars', 'debit_amt', 'credit_amt', 'balance']
        # fields = ['gl_date', 'acc_coa', 'acc_coa_ref', 'debit_amt', 'credit_amt']

    # Custom method for formatting balance
    def get_balance(self, obj):
        balance = obj.balance  # Ensure balance is accessed correctly
        # print(f"Balance value: {balance}")  # Debugging output
        # Format negative numbers as (100) and positive numbers normally
        return f"({abs(balance)})" if balance < 0 else f"{balance}"
    
class TrialBalanceSerializer(serializers.Serializer):
    acc_coa = serializers.IntegerField()
    title = serializers.CharField()
    debit_amt = serializers.DecimalField(max_digits=12, decimal_places=2)
    credit_amt = serializers.DecimalField(max_digits=12, decimal_places=2)
    opening_debit_amt = serializers.DecimalField(max_digits=12, decimal_places=2)
    opening_credit_amt = serializers.DecimalField(max_digits=12, decimal_places=2)
    closing_debit_amt = serializers.DecimalField(max_digits=12, decimal_places=2)
    closing_credit_amt = serializers.DecimalField(max_digits=12, decimal_places=2)

class AccountVoucherDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = AccountVoucherDetails
        exclude = ['created_by','updated_by','created_at','updated_at','status']

class AccountVoucherDetailViewSerializer(serializers.ModelSerializer):
    acc_coa = CostofAccountListSerializer(read_only=True)
    class Meta:
        model = AccountVoucherDetails
        exclude = ['created_by','updated_by','created_at','updated_at','status','acc_voucher_mst','institution','branch']

    def to_representation(self, instance):
        if instance.status:
            return super().to_representation(instance)
        else:
            return None

class AccountVoucherMasterViewSerializer(serializers.ModelSerializer):
    acc_voucher_detail = AccountVoucherDetailViewSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = AccountVoucherMaster
        exclude = ['created_by','updated_by','created_at','updated_at','status','branch','institution']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Filter out None values from the social_media list 
        representation['acc_voucher_detail'] = [item for item in representation['acc_voucher_detail'] if item is not None]

        if not instance.status:
            # If status is False, exclude the social_media field
            representation.pop('acc_voucher_detail', None)

        return representation

class AccountVoucherMasterSerializer(serializers.ModelSerializer):
    acc_voucher_detail = AccountVoucherDetailSerializer(many=True)

    class Meta:
        model = AccountVoucherMaster
        exclude = ['created_by','updated_by','created_at','updated_at','status']

    def validate(self, data):
        voucher_type = data.get('voucher_type')
        details = data.get('acc_voucher_detail', [])

        total_debit = sum(detail['debit_amt'] or 0 for detail in details)
        total_credit = sum(detail['credit_amt'] or 0 for detail in details)

        if voucher_type == 'PAYMENT' and total_debit != total_credit:
            raise ValidationError("For PAYMENT vouchers, the debit and credit amount must be equal.")
        
        if voucher_type == 'RECEIVE' and total_debit != total_credit:
            raise ValidationError("For RECEIVE vouchers, the total debit and credit amount must be equal.")
        
        if voucher_type == 'JOURNAL' and total_debit != total_credit:
            raise ValidationError("For JOURNAL vouchers, the total debit and credit amounts must be equal.")
        
        return data
    
    def create(self, validated_data):
        details_data = validated_data.pop('acc_voucher_detail')
        voucher = AccountVoucherMaster.objects.create(**validated_data)
        
        for detail_data in details_data:
            AccountVoucherDetails.objects.create(acc_voucher_mst=voucher, **detail_data,institution=voucher.institution,branch=voucher.branch)
        
        return voucher
    
    def update(self, instance, validated_data):
        acc_voucher_details = validated_data.pop('acc_voucher_detail')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        keep_choices = []
        for acc_voucher_detail in acc_voucher_details:
            print(acc_voucher_detail)
            if "id" in acc_voucher_detail.keys():
                if AccountVoucherDetails.objects.filter(id=acc_voucher_detail["id"]).exists():
                    c = AccountVoucherDetails.objects.get(id=acc_voucher_detail["id"])
                    c.line_no = acc_voucher_detail.get('line_no', c.line_no)
                    c.acc_coa = acc_voucher_detail.get('acc_coa', c.acc_coa)
                    c.acc_bank = acc_voucher_detail.get('acc_bank', c.acc_bank)
                    c.debit_amt = acc_voucher_detail.get('debit_amt', c.debit_amt)
                    c.credit_amt = acc_voucher_detail.get('credit_amt', c.credit_amt)
                    c.particulars = acc_voucher_detail.get('particulars', c.particulars)
                    c.status = True
                    c.save()
                    keep_choices.append(c.id)
                else:
                    continue
            else:
                c = AccountVoucherDetails.objects.create(**acc_voucher_detail, acc_voucher_mst=instance,institution=instance.institution,branch=instance.branch)
                keep_choices.append(c.id)

            for voucher in AccountVoucherDetails.objects.filter(acc_voucher_mst=instance):
                if voucher.id not in keep_choices:
                    voucher.status = False
                    voucher.save()

        return instance

class AccountBanksCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountBanks
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at','status']

class AccountBanksViewSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    bank = AccountBankViewSerializer(read_only=True)
    class Meta:
        model = AccountBanks
        exclude = ['created_by', 'updated_by','status','institution','branch']

class AccountBanksSerializer(serializers.ModelSerializer):
    bank = AccountBankViewSerializer(read_only=True)
    class Meta:
        model = AccountBanks
        fields = ['id', 'code','bank','branch_name','account_no']

