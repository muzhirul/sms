from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from .models import *

class CostofAccountSerializer(serializers.ModelSerializer):
    sub_coa = RecursiveField(many=True,required=False)

    class Meta:
        model = ChartofAccounts
        fields = ['id','coa_type','code','title','keyword','sub_coa']

class ChartOfAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartofAccounts
        fields = ['id', 'title', 'code']


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
    class Meta:
        model = AccountVoucherDetails
        exclude = ['created_by','updated_by','created_at','updated_at','status']

class AccountVoucherDetailViewSerializer(serializers.ModelSerializer):
    acc_coa = CostofAccountListSerializer(read_only=True)
    class Meta:
        model = AccountVoucherDetails
        exclude = ['created_by','updated_by','created_at','updated_at','status']

class AccountVoucherMasterViewSerializer(serializers.ModelSerializer):
    acc_voucher_detail = AccountVoucherDetailViewSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = AccountVoucherMaster
        exclude = ['created_by','updated_by','created_at','updated_at','status','branch','institution']

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


