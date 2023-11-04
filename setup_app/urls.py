from django.urls import path, include
from .views import *

urlpatterns = [
    path('api/religion/list', ReligionList.as_view(), name='religion-list'),
    path('api/bloodgroup/list', BloodGroupList.as_view(), name='blood-group-list'),
    path('api/gender/list', GenderList.as_view(), name='gender-list'),
    path('api/occupation/list', OccupationList.as_view(), name='occupation-list'),
    path('api/relation/list', RelationList.as_view(), name='relation-list'),
    path('api/day/list', DayList.as_view(), name='day-list'),
    path('api/floor/list', FloorList.as_view(), name='floor-list'),
    path('api/subject-type/list', SubjectTypeList.as_view(),
         name='subject-type-list'),
    # For Education Board
    path('api/board/list', EduBoardList.as_view(), name='education-board-list'),
    path('api/board', BoardCreateList.as_view(), name='Board-create-list'),
    path('api/board/detail/<int:pk>', BoardDetail.as_view(), name='board-detail'),
    path('api/board/delete/<int:pk>', BoardDelete.as_view(), name='board-delete'),
    # For District
    path('api/district/list', DistrictList.as_view(), name='district-list'),
    path('api/district', DistrictCreateList.as_view(),
         name='district-create-list'),
    path('api/district/detail/<int:pk>',
         DistrictDetail.as_view(), name='district-detail'),
    path('api/district/delete/<int:pk>',
         DistrictDelete.as_view(), name='district-delete'),
    # For Country
    path('api/country/list', CountryList.as_view(), name='country-list'),
    path('api/country', CountryCreateList.as_view(), name='country-create-list'),
    path('api/country/detail/<int:pk>',
         CountryDetail.as_view(), name='country-detail'),
    path('api/country/delete/<int:pk>',
         CountryDelete.as_view(), name='country-delete'),
    # For Thana
    path('api/thana/list', ThanaList.as_view(), name='thana-list'),
    path('api/thana', ThanaCreateList.as_view(), name='thana-create-list'),
    path('api/thana/detail/<int:pk>', ThanaDetail.as_view(), name='thana-detail'),
    path('api/thana/delete/<int:pk>', ThanaDelete.as_view(), name='thana-delete'),

]
