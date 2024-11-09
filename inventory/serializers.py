from rest_framework import serializers
from .models import *

'''For Warehouse'''

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

'''For Brand'''   

class BrandCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ['keyword','status','created_by', 'updated_by', 'created_at', 'updated_at']

class BrandViewSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Brand
        fields = ['id', 'name', 'keyword', 'description','is_active','status','created_username', 'updated_username', 'created_at', 'updated_at']

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return None

class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id','name','keyword']

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return None

'''For Category'''

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['keyword','status','created_by', 'updated_by', 'created_at', 'updated_at']

class CategoryViewSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Category
        fields = ['id', 'name', 'keyword', 'description','is_active','status','created_username', 'updated_username', 'created_at', 'updated_at']

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return None

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','keyword']

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return None

'''For Model'''

class ModelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        exclude = ['keyword','status','created_by', 'updated_by', 'created_at', 'updated_at']

class ModelViewSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Model
        fields = ['id', 'name', 'keyword', 'description','is_active','status','created_username', 'updated_username', 'created_at', 'updated_at']

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return None

class ModelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['id','name','keyword']

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return None

'''For Item'''

class ItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ['keyword','status','created_by', 'updated_by', 'created_at', 'updated_at']

class ItemViewSerializer(serializers.ModelSerializer):
    brand = BrandListSerializer(read_only=True)
    category = CategoryListSerializer(read_only=True)
    model = ModelListSerializer(read_only=True)
    default_warehouse = WarehouseListSerializer(read_only=True)
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Item
        # fields = ['id', 'name', 'keyword', 'description','is_active','status','created_username', 'updated_username', 'created_at', 'updated_at']
        exclude = ['status','created_by', 'updated_by', 'created_at', 'updated_at','institution','branch','sales_item','sales_uom','min_sales_qty','def_sales_price']

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return None

class ItemListSerializer(serializers.ModelSerializer):
    brand = BrandListSerializer(read_only=True)
    category = CategoryListSerializer(read_only=True)
    model = ModelListSerializer(read_only=True)
    class Meta:
        model = Item
        fields = ['id','name','keyword','brand','category','model']

    def to_representation(self, instance):
        # Only include instances where status is True
        if instance.status:
            return super().to_representation(instance)
        else:
            # If status is False, return an empty dictionary
            return None
        
class ItemShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id','code','name','def_pur_unit_price']

