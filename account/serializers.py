from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from .models import *

class CostofAccountSerializer(serializers.ModelSerializer):
    sub_coa = RecursiveField(many=True,required=False)

    class Meta:
        model = ChartofAccounts
        fields = ['id','coa_type','code','title','keyword','sub_coa']

class AccLedgerSerializer(serializers.ModelSerializer):
    cumulative_balance = serializers.FloatField(read_only=True)

    class Meta:
        model = AccountLedger
        fields = ['gl_date', 'acc_coa', 'acc_coa_ref', 'debit_amt', 'credit_amt', 'cumulative_balance']