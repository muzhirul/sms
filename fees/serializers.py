from rest_framework import serializers
from .models import *

class FeesTypeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeesType
        exclude = ['status','created_by','updated_by','created_at','updated_at']

class FeesTypeViewSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = FeesType
        exclude = ['status','institution','branch','created_by','updated_by']


class FeesDiscountCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeesDiscount
        exclude = ['status','created_by','updated_by','created_at','updated_at']

class FeesDiscountViewSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = FeesDiscount
        exclude = ['status','institution','branch','created_by','updated_by']