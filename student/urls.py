from django.urls import path,include
from .views import *


urlpatterns = [
    path('api/student', StudentList.as_view(), name='student-list'),
    path('api/short/list', StudentShortList.as_view(), name='student-short-list'),
    path('api/student/detail/<int:pk>', StudentDetail.as_view(), name='student-detail'),
    path('api/student/image/<int:pk>', StudentImageUpload.as_view(), name='student-image-upload'),
    path('api/guardian/image/<int:pk>', GuardianImageUpload.as_view(), name='guardian-image-upload'),
    path('api/student-teacher/list', StudentWiseTeacherList.as_view(), name="student-wise-teacher-list"),
    # Student Attendance Process
    path('api/attendance/process', StudentAttendanceProcess.as_view(), name='student-attendance-process'),
    # path('api/attendance/update/process', StudentAttendanceUpdateProcess.as_view(), name='student-attendance-update-process'),
    path('api/attendance/search', StudentAttendanceSearch.as_view(), name='student-attendance-search'),
    path('api/attendance/update/<int:pk>', StudentAttendanceUpdate.as_view(), name='student-attendance-update'),
    # Student Leave 
    path('api/leave/create', StudentLeaveCreate.as_view(), name='student-leave-create'),
    path('api/leave/list', StudentLeaveList.as_view(), name='student-leave-List'),
    path('api/leave/detail/<int:pk>', StudentLeaveDetails.as_view(), name='student-leave-details'),
    path('api/responsible/leave/list', StudentResponsibleLeaveList.as_view(), name='student-responsible-leave-list'),
    # Teacher Wise Student List
    path('api/teacher-wise', TeacherWiseStudentList.as_view(), name='teacher-wise-student'),
    # stuent Status Transaction
    path('api/std-status/trns/create',StudentStatusCreate.as_view(), name='student-status-trns-create-list'),
    # Student attendance List
    path('api/daily/attn-list',StudentDailyAttnList.as_view(), name='staff-daily-attn-list'),
]