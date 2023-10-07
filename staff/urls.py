from django.urls import path,include
from .views import StaffDepartmentListCreate

urlpatterns = [
    path('api/department', StaffDepartmentListCreate.as_view(), name='staff-department-list-create'),
]