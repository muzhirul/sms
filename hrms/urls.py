from django.urls import path
from .views import *

urlpatterns = [
    # For account bank
    path('api/bank/list', BankList.as_view(), name='bank-list'),
    path('api/bank', BankCreateList.as_view(), name='bank-list-create'),
    path('api/bank/detail/<int:pk>', BankDetail.as_view(), name='bank-detail'),
    path('api/bank/delete/<int:pk>', BankDelete.as_view(), name='Bank-delete'),
    # For Holiday
    path('api/holiday/list', HolidayListView.as_view(), name='holiday-View-list'),
    path('api/holiday', HolidayCreateList.as_view(), name='holiday-list-create'),
    path('api/holiday/detail/<int:pk>', HolidayDetail.as_view(), name='holiday-detail'),
    path('api/holiday/delete/<int:pk>', HolidayDelete.as_view(), name='holiday-delete'),
    # For Leave Type
    path('api/leave-type/list', LeaveTypeList.as_view(), name='leave-type-list'),
    path('api/leave-type', LeaveTypeCreateList.as_view(), name='leave-type-list-create'),
    path('api/leave-type/detail/<int:pk>', LeaveTypeDetail.as_view(), name='leave-type-detail'),
    path('api/leave-type/delete/<int:pk>', LeaveTypeDelete.as_view(), name='leave-type-delete'),
    # For Salary Setup
    path('api/salary-setup/list', SalarySetupList.as_view(), name='salary-setup-list'),
    path('api/salary-all-element/list',SalaryElementList.as_view(), name='salary-element-list'),
    path('api/salary-element/list',SalarySpecificElementList.as_view(), name='salary-specific-element-list'),
    path('api/salary-setup/create', SalarySetupCreate.as_view(), name='salary-setup-create'),
]