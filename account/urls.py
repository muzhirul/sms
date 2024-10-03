from django.urls import path
from .views import *

urlpatterns = [
    path('api/chart-of-accounts/list',ChartofAccountList.as_view(), name='chart_of_accounts_list'),
    path('api/ledger', AccLedgerListView.as_view(), name='acc_ledger_list'),
]