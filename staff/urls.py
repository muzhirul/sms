from django.urls import path, include
from .views import *

urlpatterns = [
    # Department api
    path('api/department', StaffDepartmentListCreate.as_view(),
         name='staff-department-list-create'),
    path('api/department/list', StaffDepartmentList.as_view(),
         name='staff-department-list'),
    path('api/department/detail/<int:pk>',
         DepartmentDetail.as_view(), name='department-detail'),
    path('api/department/delete/<int:pk>',
         DepartmentDelete.as_view(), name='department-delete'),
    # Designation API
    path('api/designation', StaffDesignationListCreate.as_view(),
         name='staff-designation-list-create'),
    path('api/designation/list', StaffDesignationList.as_view(),
         name='staff-designation-list'),
    path('api/designation/detail/<int:pk>',
         DesignationDetail.as_view(), name='designation-detail'),
    path('api/designation/delete/<int:pk>',
         DesignationDelete.as_view(), name='designation-delete'),
    # staff API
    path('api/create', staffCreateView.as_view(), name='staff-create'),
    path('api/list', staffListView.as_view(), name='staff-List'),

    # staff shift API
    path('api/shift', StaffShiftListCreate.as_view(),
         name='staff-shift-list-create'),
    path('api/shift/detail/<int:pk>',
         StaffShiftDetail.as_view(), name='staff-shift-detail'),
    path('api/shift/delete/<int:pk>',
         StaffShiftDelete.as_view(), name='staff-shift-delete'),
]
