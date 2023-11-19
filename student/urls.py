from django.urls import path,include
from .views import *


urlpatterns = [
    path('api/student', StudentList.as_view(), name='student-list'),
    path('api/student/detail/<int:pk>', StudentDetail.as_view(), name='student-detail'),
    path('api/student/image/<int:pk>', StudentImageUpload.as_view(), name='student-image-upload'),
    path('api/guardian/image/<int:pk>', GuardianImageUpload.as_view(), name='guardian-image-upload'),
]