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

class AccLedgerSerializer(serializers.ModelSerializer):
    acc_coa = CostofAccountListSerializer(read_only=True)
    acc_coa_ref = CostofAccountListSerializer(read_only=True)
    balance = serializers.SerializerMethodField()

    class Meta:
        model = AccountLedger
        fields = ['gl_date', 'acc_coa', 'acc_coa_ref','narration','particulars', 'debit_amt', 'credit_amt', 'balance']
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


