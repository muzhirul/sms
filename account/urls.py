from django.urls import path
from .views import *

urlpatterns = [
    path('api/chart-of-accounts/list',ChartofAccountList.as_view(), name='chart_of_accounts_list'),
    path('api/ledger', AccLedgerListView.as_view(), name='acc_ledger_list'),
    path('api/coa/head/list', COAHeadList.as_view(), name='coa_head_list'),
    path('api/trial-balance', TrialBalanceAPIView.as_view(), name='acc_trial_balance_list'),
]