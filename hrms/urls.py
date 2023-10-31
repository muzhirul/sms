from django.urls import path
from .views import *

urlpatterns = [
    # For account bank
    path('api/bank', BankCreateList.as_view(), name='bank-list-create'),
    path('api/bank/detail/<int:pk>', BankDetail.as_view(), name='bank-detail'),
    path('api/bank/delete/<int:pk>', BankDelete.as_view(), name='Bank-delete'),
]