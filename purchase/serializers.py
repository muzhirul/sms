from rest_framework import serializers
from .models import *
from setup_app.serializers import *
from hrms.serializers import *

'''For Suppliers'''

class SupplierViewSerializer(serializers.ModelSerializer):
    bank = AccountBankViewSerializer(read_only=True)
    thana = ThanaViewSerializer(read_only=True)
    district = DistrictdViewSerializer(read_only=True)
    division = DivisionViewSerializer(read_only=True)
    country = CountryViewSerializer(read_only=True)
    class Meta:
        model = Supplier
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at','institution','branch']

class SupplierCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']

class SupplierListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id','name','short_name']

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return None