from django.urls import path,include
from .views import (StaffDepartmentListCreate,StaffDepartmentList, DepartmentDetail,DepartmentDelete)

urlpatterns = [
    path('api/department', StaffDepartmentListCreate.as_view(), name='staff-department-list-create'),
    path('api/department/list', StaffDepartmentList.as_view(), name='staff-department-list'),
    path('api/department/detail/<int:pk>', DepartmentDetail.as_view(), name='department-detail'),
    path('api/department/delete/<int:pk>', DepartmentDelete.as_view(), name='department-delete'),
]