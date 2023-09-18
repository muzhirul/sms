from django.urls import path,include
from .views import (StudentList,StudentDetail)


urlpatterns = [
    path('api/student', StudentList.as_view(), name='student-list'),
    path('api/student/detail/<int:pk>', StudentDetail.as_view(), name='student-detail'),
]