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
    path('api/search/', staffSearchView.as_view(), name='staff-search'),
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
    path('api/raw/attendance', staffSpecificRawAttendance.as_view(), name='staff-specific-attendance'),
    # Staff Self Attendance Entry
    path('api/self-attendance', StaffSelfAttendanceEntry.as_view(), name='staff-self-attendance-entry'),
    # Staff Leaave Transaction
    path('api/leave/balance/list', StaffLeaveList.as_view(), name='staff-leave-list'),
    path('api/leave-trns/create', staffLeaveTransactionCreate.as_view(), name='staff-leave-transaction-create'), 
    path('api/leave-trns/detail/<int:pk>', staffLeaveTransactionUpdate.as_view(), name='staff-leave-transaction-update'), 
    path('api/leave-trns/view/<int:pk>', staffLeaveTransactionList.as_view(), name='staff-leave-transaction-List'), 
    path('api/leave/status/<str:staff_id>', staffLeaveStatusList.as_view(), name='staff-leave-status-list'),
    path('api/leave-trns/all', StaffLeaveTrnsAlllLst.as_view(), name='staff-leave-transaction-all-list'),
    path('api/personal/leave-trns', StaffLeaveTrnsPersonallLst.as_view(), name='staff-leave-transaction-personal-list'),
    path('api/leave-trns/<str:staff_id>', StaffLeaveTrnslLst.as_view(), name='staff-leave-transaction-list'),
    # Staff Leave Type base on assign 
    path('api/leave-type/list', StaffLeaveTypeList.as_view(), name='staff-leave-type-list'),
    # Retrive Data From Puntch 
    path('api/punch/data', StaffPunchData.as_view(), name='punch-data-retrive'),
    # Staff attendance master table Process
    path('api/attendance-summery/process', StaffAttendanceSummeryProcess.as_view(), name='staff-attn-summery-process'),
    # Staff Status Transaction
    path('api/status/trns/create',StaffStatusCreate.as_view(), name='staff-status-trns-create-list'),
    # Staff Leave History
    path('api/leave-approval/<int:pk>',StaffLeaveHistoryUpdate.as_view(), name='staff-leave-history-update'),
    # Staff attendance List
    path('api/daily/attn-list',StaffDailyAttnList.as_view(), name='staff-daily-attn-list'),
    # Staff payroll process
    path('api/payroll/process', StaffPayrollProcess.as_view(), name='staff-payroll-process'),
    
]
