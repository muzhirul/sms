from django.urls import path
from .views import *

urlpatterns = [
    path('api/coa/create', ChartOfAccountCreateList.as_view() ,name="chart-of-accounts-create-list"),
    path('api/chart-of-accounts/list',ChartofAccountList.as_view(), name='chart_of_accounts_list'),
    path('api/ledger', AccLedgerListView.as_view(), name='acc_ledger_list'),
    path('api/coa/head/list', COAHeadList.as_view(), name='coa_head_list'),
    path('api/trial-balance', TrialBalanceAPIView.as_view(), name='acc_trial_balance_list'),
    path('api/acc-general-ledger/list', AccountGenLedgerListView.as_view(), name='acc_general_ledger_list'),
    path('api/all-voucher', AccountVoucherCreateAPIView.as_view(), name='account-voucher-create'),
    path('api/voucher/detail/<int:pk>', AccountVoucherDetaillupdate.as_view(), name='account-voucher-detail'),
    path('api/account-voucher/delete/<int:pk>', AccountVoucherDelete.as_view(), name='account-voucher-delete'),
    path('api/account-voucher/confirm/<int:pk>', AccountVoucherConfirm.as_view(), name='account-voucher-confirm'),
    path('api/voucher-master/list', AccountVoucherMasterAPIView.as_view(), name='account-voucher-master'),
    path('api/voucher-details/list', AccountVoucherDetailAPIView.as_view(), name='account-voucher-details'),
    path('api/voucher-all/list', AccountVoucherAllAPIView.as_view(), name='account-voucher-all'),
    # For Account Bank
    path('api/bank/list', AccountBankList.as_view(), name='account-bank-list'),
    path('api/bank/create', AccountBankCreateList.as_view(), name='account-bank-create-list'),
    path('api/bank/detail/<int:pk>', AccountBankDetail.as_view(), name='bank-detail'),
    path('api/bank/delete/<int:pk>', AccountBankDelete.as_view(), name='bank-delete'),
]