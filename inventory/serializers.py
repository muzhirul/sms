from rest_framework import serializers
from .models import *

class WarehouseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']

class WarehouseViewSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'keyword', 'description','address','category','as_default','is_active','status','created_username', 'updated_username', 'created_at', 'updated_at']

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return None

class WarehouseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id','name','category']

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return None