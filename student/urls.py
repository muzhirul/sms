from django.urls import path,include
from .views import *


urlpatterns = [
    path('api/student', StudentList.as_view(), name='student-list'),
    path('api/student/detail/<int:pk>', StudentDetail.as_view(), name='student-detail'),
    path('api/student/image/<int:pk>', StudentImageUpload.as_view(), name='student-image-upload'),
    path('api/guardian/image/<int:pk>', GuardianImageUpload.as_view(), name='guardian-image-upload'),
    # Student Attendance Process
    path('api/attendance/process', StudentAttendanceProcess.as_view(), name='student-attendance-process'),
    # path('api/attendance/update/process', StudentAttendanceUpdateProcess.as_view(), name='student-attendance-update-process'),
    path('api/attendance/search', StudentAttendanceSearch.as_view(), name='student-attendance-search'),
    path('api/attendance/update/<int:pk>', StudentAttendanceUpdate.as_view(), name='student-attendance-update'),
    # Student Leave 
    path('api/leave/create', StudentLeaveCreate.as_view(), name='student-leave-create'),
    path('api/leave/list', StudentLeaveList.as_view(), name='student-leave-List'),
    path('api/leave/detail/<int:pk>', StudentLeaveDetails.as_view(), name='student-leave-details'),
    # Teacher Wise Student List
    path('api/teacher-wise', TeacherWiseStudentList.as_view(), name='teacher-wise-student'),
]