from django.urls import path
from .views import *

urlpatterns = [
    path('api/chart-of-accounts/list',ChartofAccountList.as_view(), name='chart_of_accounts_list'),
    path('api/ledger', AccLedgerListView.as_view(), name='acc_ledger_list'),
    path('api/coa/head/list', COAHeadList.as_view(), name='coa_head_list'),
    path('api/trial-balance', TrialBalanceAPIView.as_view(), name='acc_trial_balance_list'),
    path('api/acc-general-ledger/list', AccountGenLedgerListView.as_view(), name='acc_general_ledger_list'),
    path('api/all-voucher', AccountVoucherCreateAPIView.as_view(), name='account-voucher-create'),
    path('api/voucher/detail/<int:pk>', AccountVoucherDetaillupdate.as_view(), name='account-voucher-detail'),
    path('api/account-voucher/delete/<int:pk>', AccountVoucherDelete.as_view(), name='account-voucher-delete'),
    path('api/voucher-master/list', AccountVoucherMasterAPIView.as_view(), name='account-voucher-master'),
    path('api/voucher-details/list', AccountVoucherDetailAPIView.as_view(), name='account-voucher-details')
]