from rest_framework import serializers
from .models import *
from setup_app.serializers import *
from hrms.serializers import *
from inventory.serializers import *

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

'''For Purchase order'''    

class PurchaseOrderDetailsCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = PurchaseOrderDetails
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']

class PurchaseOrderDetailsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderDetails
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']

    def to_representation(self, instance):
        if instance.status:
            return super().to_representation(instance)
        else:
            return None
        
class PurchaseOrderMasterViewSerializer(serializers.ModelSerializer):
    supplier = SupplierListSerializer(read_only=True)
    warehouse = WarehouseListSerializer(read_only=True)
    pay_method = PaymentMethodViewSerializer(read_only=True)
    order_details = PurchaseOrderDetailsViewSerializer(many=True)
    class Meta:
        model = PurchaseOrderMaster
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at','institution','branch']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Filter out None values from the social_media list 
        representation['order_details'] = [item for item in representation['order_details'] if item is not None]

        if not instance.status:
            # If status is False, exclude the social_media field
            representation.pop('order_details', None)

        return representation

class PurchaseOrderMasterCreateSerializer(serializers.ModelSerializer):
    order_details = PurchaseOrderDetailsCreateSerializer(many=True)
    class Meta:
        model = PurchaseOrderMaster
        exclude = ['code','total_ord_qty','total_dis_amt','total_ord_amt','created_by', 'updated_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        order_details = validated_data.pop('order_details')
        order = PurchaseOrderMaster.objects.create(**validated_data)

        for order_detail in order_details:
            PurchaseOrderDetails.objects.create(order_mst=order, **order_detail, institution=order.institution,branch=order.branch)

        return order
    
    def update(self, instance, validated_data):
        order_details = validated_data.pop('order_details')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        keep_choices = []
        # Fields to update in order details
        fields_to_update = [
            'line', 'item', 'order_qty', 'approve_qty', 'receive_qty', 'uom', 'unit_price',
            'other_cost', 'vat_pct', 'vat_amt', 'dis_pct', 'dis_amt', 'remarks', 'is_active'
        ]

        for order_detail in order_details:
            if "id" in order_detail:
                try:
                    o = PurchaseOrderDetails.objects.get(id=order_detail["id"])
                    for field in fields_to_update:
                        setattr(o, field, order_detail.get(field, getattr(o, field)))
                    o.status = True
                    o.save()
                    keep_choices.append(o.id)
                except PurchaseOrderDetails.DoesNotExist:
                    continue
            else:
                o = PurchaseOrderDetails.objects.create(
                    **order_detail,
                    order_mst=instance,
                    institution=instance.institution,
                    branch=instance.branch
                )
                keep_choices.append(o.id)

        # Deactivate any remaining order details not in keep_choices
        PurchaseOrderDetails.objects.filter(order_mst=instance).exclude(id__in=keep_choices).update(status=False)

        return instance


'''For GRN '''    

class GoodsReceiptNotesDetailsCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = GoodsReceiptNotesDetails
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at','status','institution','branch']
        read_only_fields = ('goods_receipt_note',)

class GoodsReceiptNotesDetailsViewSerializer(serializers.ModelSerializer):
    item = ItemShortSerializer(read_only=True)
    class Meta:
        model = GoodsReceiptNotesDetails
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at','institution','branch','status','goods_receipt_note']

    def to_representation(self, instance):
        if instance.status:
            return super().to_representation(instance)
        else:
            return None
        
class GoodSReceiptNoteMasterViewSerializer(serializers.ModelSerializer):
    supplier = SupplierListSerializer(read_only=True)
    warehouse = WarehouseListSerializer(read_only=True)
    pay_method = PaymentMethodViewSerializer(read_only=True)
    grn_details = GoodsReceiptNotesDetailsViewSerializer(many=True)
    class Meta:
        model = GoodSReceiptNoteMaster
        exclude = ['created_by', 'updated_by', 'created_at', 'updated_at','institution','branch']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Filter out None values from the social_media list 
        representation['grn_details'] = [item for item in representation['grn_details'] if item is not None]

        if not instance.status:
            # If status is False, exclude the social_media field
            representation.pop('grn_details', None)

        return representation

class GoodSReceiptNoteMasterCreateSerializer(serializers.ModelSerializer):
    grn_details = GoodsReceiptNotesDetailsCreateSerializer(many=True)
    class Meta:
        model = GoodSReceiptNoteMaster
        exclude = ['status','code','total_rec_qty','total_dis_amt','total_rec_amt','total_net_amt','created_by', 'updated_by', 'created_at', 'updated_at','institution','branch']

    def create(self, validated_data):
        grn_details = validated_data.pop('grn_details')
        order = GoodSReceiptNoteMaster.objects.create(**validated_data)

        for grn_detail in grn_details:
            GoodsReceiptNotesDetails.objects.create(goods_receipt_note=order, **grn_detail, institution=order.institution,branch=order.branch)

        return order
    
    def update(self, instance, validated_data):
        grn_details = validated_data.pop('grn_details')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        keep_choices = []
        # Fields to update in order details
        fields_to_update = [
            'line_no', 'item', 'rcv_qty', 'rcv_uom', 'rcv_rate', 'rcv_amt', 'net_total_amt',
            'remarks', 'is_active'
        ]

        for grn_detail in grn_details:
            if "id" in grn_detail:
                try:
                    o = GoodsReceiptNotesDetails.objects.get(id=grn_detail["id"])
                    for field in fields_to_update:
                        setattr(o, field, grn_detail.get(field, getattr(o, field)))
                    o.status = True
                    o.save()
                    keep_choices.append(o.id)
                except GoodsReceiptNotesDetails.DoesNotExist:
                    continue
            else:
                print(grn_detail,'****************')
                o = GoodsReceiptNotesDetails.objects.create(
                    **grn_detail,
                    goods_receipt_note=instance,
                    institution=instance.institution,
                    branch=instance.branch
                )
                keep_choices.append(o.id)

        # Deactivate any remaining order details not in keep_choices
        GoodsReceiptNotesDetails.objects.filter(goods_receipt_note=instance).exclude(id__in=keep_choices).update(status=False)

        return instance

class GoodSReceiptNoteMasterDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodSReceiptNoteMaster
        fields = ['status']

