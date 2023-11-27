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


class DivisionViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Division
        fields = ['id', 'divi_code', 'name']


class DivisionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Division
        exclude = ['status', 'created_by','updated_by', 'created_at', 'updated_at']


class DivisionSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    country = CountryViewSerializer(read_only=True)

    class Meta:
        model = Division
        exclude = ['status']


class DistrictdViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = ['id', 'dist_code', 'name']


class DistrictCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        exclude = ['status', 'created_by','updated_by', 'created_at', 'updated_at']


class DistrictSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    division = DivisionViewSerializer(read_only=True)

    class Meta:
        model = District
        exclude = ['status']


class ThanaViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thana
        fields = ['id', 'thana_code', 'name']


class ThanaCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thana
        exclude = ['status', 'created_by', 'updated_by', 'created_at', 'updated_at']


class ThanaSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    district = DistrictdViewSerializer()

    class Meta:
        model = Thana
        exclude = ['status']

class ContractTypeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractType
        fields = ['id','name']

class MaritalStatusViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaritalStatus
        fields = ['id','name']
