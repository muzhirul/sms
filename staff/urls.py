from django.urls import path, include
from .views import *

urlpatterns = [
    # Department api
    path('api/department', StaffDepartmentListCreate.as_view(),name='staff-department-list-create'),
    path('api/department/list', StaffDepartmentList.as_view(),name='staff-department-list'),
    path('api/department/detail/<int:pk>',DepartmentDetail.as_view(), name='department-detail'),
    path('api/department/delete/<int:pk>',DepartmentDelete.as_view(), name='department-delete'),
    # Designation API
    path('api/designation', StaffDesignationListCreate.as_view(),name='staff-designation-list-create'),
    path('api/designation/list', StaffDesignationList.as_view(),name='staff-designation-list'),
    path('api/designation/detail/<int:pk>',DesignationDetail.as_view(), name='designation-detail'),
    path('api/designation/delete/<int:pk>',DesignationDelete.as_view(), name='designation-delete'),
    # staff API
    path('api/create', staffCreateView.as_view(), name='staff-create'),
    path('api/list', staffListView.as_view(), name='staff-List'),
    path('api/less-dtl/list', staffLessDtlListView.as_view(), name='staff-List'),
    path('api/teacher/list', staffTeacherListView.as_view(), name='teacher-List'),
    path('api/detail/<int:pk>', staffDetailView.as_view(), name='staff-detail'),
    path('api/image/<int:pk>', StaffImageUpload.as_view(), name='staff-image-upload'),
    path('api/role-base-staff/<str:role_id>', staffRoleBaseSataffListView.as_view(), name='role-base-staff-List'),
    path('api/search/staff/list', StaffSearchList.as_view(), name='search-staff-list'),

    # staff shift API
    path('api/shift/list', StaffShiftList.as_view(),name='shift-list'),
    path('api/shift', StaffShiftListCreate.as_view(),name='staff-shift-list-create'),
    path('api/shift/detail/<int:pk>',StaffShiftDetail.as_view(), name='staff-shift-detail'),
    path('api/shift/delete/<int:pk>',StaffShiftDelete.as_view(), name='staff-shift-delete'),

    # Staff Attendance Process
    path('api/attendance/process', StaffAttendanceProcess.as_view(), name='staff-attendance-process'),
    path('api/attendance/update/process', StaffAttendanceUpdateProcess.as_view(), name='staff-attendance-update-process'),
    # Staff Raw Attendance Entry
    path('api/raw/attendance/entry', StaffAttendanceEntry.as_view(), name='staff-attendance-entry'),
    path('api/raw/attendance/list', staffRawAttendanceList.as_view(), name='staff-raw-attendance-list'),
    # Staff Leaave 
    # path('/api/leave/list', )
]
