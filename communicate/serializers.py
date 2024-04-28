from rest_framework import serializers
from .models import *
from setup_app.serializers import RoleSerializer

class NoticeBoardViewSerializers(serializers.ModelSerializer):
    notice_for = RoleSerializer(read_only=True,many=True)
    class Meta:
        model = NoticeBoard
        fields = ['id','title','notice_date','publish_date','attachment','description','notice_for','is_active']

    def to_representation(self, instance):
        if instance.status:
            return super().to_representation(instance)
        else:
            return None
        
class NoticeBoardCreateSerializers(serializers.ModelSerializer):
    notice_for = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), many=True)
    class Meta:
        model = NoticeBoard
        fields = '__all__'