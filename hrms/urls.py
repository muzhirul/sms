from django.urls import path
from .views import *

urlpatterns = [
    # For account bank
    path('api/bank', BankCreateList.as_view(), name='bank-list-create'),
    path('api/bank/detail/<int:pk>', BankDetail.as_view(), name='bank-detail'),
    path('api/bank/delete/<int:pk>', BankDelete.as_view(), name='Bank-delete'),
    # For Holiday
    path('api/holiday', HolidayCreateList.as_view(), name='holiday-list-create'),
    path('api/holiday/detail/<int:pk>', HolidayDetail.as_view(), name='holiday-detail'),
    path('api/holiday/delete/<int:pk>', HolidayDelete.as_view(), name='holiday-delete'),
]