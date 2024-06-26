from rest_framework import serializers
from .models import *
from academic.serializers import *
from student.serializers import *

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

class FeesTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeesType
        fields = ['id','name','code']


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

class FeesDetailsViewSerializer(serializers.ModelSerializer):
    fees_type = FeesTypeListSerializer(read_only=True)
    class Meta:
        model = FeesDetails
        exclude = ['fees_master','status','created_at','updated_at','created_by','updated_by','institution','branch']

    def to_representation(self, instance):
        if instance.status:
            return super().to_representation(instance)
        else:
            return None

class FeesDetailsCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False) 

    class Meta:
        model = FeesDetails
        exclude = ['status','created_at','updated_at','created_by','updated_by']

class FeesMasterCreateSerializer(serializers.ModelSerializer):
    fees_detail = FeesDetailsCreateSerializer(many=True)

    class Meta:
        model = FeesMaster
        exclude = ['status','created_at','updated_at','created_by','updated_by']

    def update(self, instance,validated_data):
        fees_details = validated_data.pop('fees_detail',[])
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        keep_dtl_id = []
        try:
            for fees_detail in fees_details:
                if "id" in fees_detail.keys():
                    if FeesDetails.objects.filter(id=fees_detail["id"]).exists():
                        f = FeesDetails.objects.get(id=fees_detail["id"])
                        f.fees_type = fees_detail.get('fees_type',f.fees_type)
                        f.due_date = fees_detail.get('due_date',f.due_date)
                        f.amount = fees_detail.get('amount',f.amount)
                        f.percentage = fees_detail.get('percentage',f.percentage)
                        f.fix_amt = fees_detail.get('fix_amt',f.fix_amt)
                        f.description = fees_detail.get('description',f.description)
                        f.remarks = fees_detail.get('remarks',f.remarks)
                        f.is_active = fees_detail.get('is_active',f.is_active)
                        f.status = True
                        f.save()
                        keep_dtl_id.append(f.id)
                    else:
                        continue
                else:
                    f = FeesDetails.objects.create(**fees_detail,fees_master=instance,institution=instance.institution,branch=instance.branch)
                    keep_dtl_id.append(f.id)
                
                for detail in instance.fees_detail.all():
                    if detail.id not in keep_dtl_id:
                        detail.status = False
                        detail.save()
        except:
            pass
        return instance

class FeesMasterViewSerializer(serializers.ModelSerializer):
    version = VersionSerializer2(read_only=True)
    section = SectionSerializer2(read_only=True)
    class_name = ClassSerializer2(read_only=True)
    session = SessionSerializer2(read_only=True)
    group = ClassGroupListSerializer(read_only=True)
    fees_detail = FeesDetailsViewSerializer(many=True)

    class Meta:
        model = FeesMaster
        exclude = ['status','created_at','updated_at','created_by','updated_by','institution','branch']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Filter out None values from the social_media list 
        representation['fees_detail'] = [item for item in representation['fees_detail'] if item is not None]

        if not instance.status:
            # If status is False, exclude the social_media field
            representation.pop('fees_detail', None)

        return representation

class FeesTransactionViewSerializer(serializers.ModelSerializer):
    fees_detail = FeesDetailsViewSerializer(read_only=True)
    pay_method = PaymentMethodViewSerializer(read_only=True)
    class Meta:
        model = FeesTransaction
        exclude = ['status','created_at','updated_at','created_by','updated_by','institution','branch']