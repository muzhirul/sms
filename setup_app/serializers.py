from rest_framework import serializers
from .models import *
from rest_framework_recursive.fields import RecursiveField


class MenuSerializer(serializers.ModelSerializer):
    sub_menu = RecursiveField(many=True, Required=False)

    class Meta:
        model: Menu
        fields = ['name', 'slug', 'icon', 'level', 'sl_no']


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model: Role
        fields = ['name']


class ReligionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Religion
        fields = ['id', 'name']


class BloodGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = BloodGroup
        fields = ['id', 'name']


class GenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gender
        fields = ['id', 'name']


class OccupationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Occupation
        fields = ['id', 'name']


class RelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Relation
        fields = ['id', 'name']


class DaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Day
        fields = ['short_name', 'long_name']


class FloorTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FloorType
        fields = ['id', 'name']


class SubjectTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubjectType
        fields = ['id', 'name']


class EducationBoardViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = EducationBoard
        fields = ['id', 'board_code', 'name']


class EducationBoardSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = EducationBoard
        exclude = ['status']


class DistrictdViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = ['id', 'dist_code', 'name']


class DistrictSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = District
        exclude = ['status']


class CountryViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ['id', 'coun_code', 'name']


class CountrySerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Country
        exclude = ['status']


class ThanaViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thana
        fields = ['id', 'thana_code', 'name']


class ThanaSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Thana
        exclude = ['status']
