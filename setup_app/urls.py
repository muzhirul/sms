from django.urls import path, include
from .views import *

urlpatterns = [
    path('api/religion/list', ReligionList.as_view(), name='religion-list'),
    path('api/bloodgroup/list', BloodGroupList.as_view(), name='blood-group-list'),
    path('api/gender/list', GenderList.as_view(), name='gender-list'),
    path('api/occupation/list', OccupationList.as_view(), name='occupation-list'),
    path('api/relation/list', RelationList.as_view(), name='relation-list'),
    path('api/floor/list', FloorList.as_view(), name='floor-list'),
    path('api/subject-type/list', SubjectTypeList.as_view(), name='subject-type-list'),
    path('api/attendance-typee/list', AttendancetypeList.as_view(), name='attendance-type-list'),
    path('api/holiday-type/list', HolidayTypeList.as_view(), name='attendance-type-list'),
    # For Education Board
    path('api/board/list', EduBoardList.as_view(), name='education-board-list'),
    path('api/board', BoardCreateList.as_view(), name='Board-create-list'),
    path('api/board/detail/<int:pk>', BoardDetail.as_view(), name='board-detail'),
    path('api/board/delete/<int:pk>', BoardDelete.as_view(), name='board-delete'),
    # For Division
    path('api/division/list', DivisionList.as_view(), name='division-list'),
    path('api/division', DivisionCreateList.as_view(),name='division-create-list'),
    path('api/division/detail/<int:pk>',DivisionDetail.as_view(), name='division-detail'),
    path('api/division/delete/<int:pk>',DivisionDelete.as_view(), name='division-delete'),
    # For District
    path('api/district/list', DistrictList.as_view(), name='district-list'),
    path('api/district', DistrictCreateList.as_view(),name='district-create-list'),
    path('api/district/detail/<int:pk>',DistrictDetail.as_view(), name='district-detail'),
    path('api/district/delete/<int:pk>',DistrictDelete.as_view(), name='district-delete'),
    # For Country
    path('api/country/list', CountryList.as_view(), name='country-list'),
    path('api/country', CountryCreateList.as_view(), name='country-create-list'),
    path('api/country/detail/<int:pk>',CountryDetail.as_view(), name='country-detail'),
    path('api/country/delete/<int:pk>',CountryDelete.as_view(), name='country-delete'),
    # For Thana
    path('api/thana/list', ThanaList.as_view(), name='thana-list'),
    path('api/thana', ThanaCreateList.as_view(), name='thana-create-list'),
    path('api/thana/detail/<int:pk>', ThanaDetail.as_view(), name='thana-detail'),
    path('api/thana/delete/<int:pk>', ThanaDelete.as_view(), name='thana-delete'),
    # For Contract Type
    path('api/contrac-type/list', ContractTypeList.as_view(), name='contrac-type-list'),
    # For Days
    path('api/day/list', DayList.as_view(), name='day-list'),
    path('api/day', DayCreateList.as_view(),name='Day-create-list'),
    path('api/day/detail/<int:pk>',DayDetail.as_view(), name='Day-detail'),
    path('api/day/delete/<int:pk>',DayDelete.as_view(), name='Day-delete'),
    # For Role 
    path('api/role/list', RoleList.as_view(), name='role-day'),
    # For MaritalStatus 
    path('api/marital-status/list', MaritalStatusList.as_view(), name='marital-status-day'),
    # Payment Method API
    path('api/pay-method/list', PayMethodList.as_view(), name='pay-method-list'),

]
