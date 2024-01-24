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
]