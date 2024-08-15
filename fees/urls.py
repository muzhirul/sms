from django.urls import path
from .views import *

urlpatterns = [
    # For Fees Type
    path('api/fees-type/list', FeesTypeList.as_view(), name='fees-type-list'),
    path('api/fees-type', FeesTypeCreateList.as_view(), name='fees-type-create-list'),
    path('api/fees-type/detail/<int:pk>', FeesTypeDetail.as_view(), name='fees-type-detail'),
    path('api/fees-type/delete/<int:pk>', FeesTypeDelete.as_view(), name='fees-type-delete'),
    # For Fees Discount
    path('api/fees-discount', FeesDiscountCreateList.as_view(), name='fees-discount-create-list'),
    path('api/fees-discount/detail/<int:pk>', FeesDiscountDetail.as_view(), name='fees-discount-detail'),
    path('api/fees-discount/delete/<int:pk>', FeesDiscountDelete.as_view(), name='fees-discount-delete'),
    # For Fees Dtails
    path('api/fees-entry/create', FeesCreateList.as_view(), name='fees-list-create'),
    path('api/fees-entry/detail/<int:pk>', FeesDetailUpdate.as_view(), name='fees-details-update'),
    # For Fees Details Break Down
    path('api/fees-dlt-break-down/create', FeesDetailsBreakDownCreate.as_view(), name='fees-dtl-break-down-create'),
    path('api/fees-dlt-break-down/list', FeesDetailsBreakDownList.as_view(), name='fees-dtl-break-down-list'),
    # For Fees Transactions
    path('api/fees-trns/manual', FeesTrnsManualEntry.as_view(), name='fees-transaction-manual-process'),
]