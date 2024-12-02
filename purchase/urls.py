from django.urls import path
from .views import *

urlpatterns = [
    # For Suppliers
    path('api/supplier/list', SupplierList.as_view(), name='supplier-list'),
    path('api/supplier', SupplierCreateList.as_view(), name='supplier-create-list'),
    path('api/supplier/detail/<int:pk>', SupplierDetail.as_view(), name='supplier-detail'),
    path('api/supplier/delete/<int:pk>', SupplierDelete.as_view(), name='supplier-delete'),
    # For Purchase Order
    path('api/purchase-order/list', PurchaseOrderList.as_view(), name='purchase-order-list'),
    # For Goods Receive Note
    path('api/goods-receive/list', GoodsReceiveNoteList.as_view(), name='goods-receive-note-list'),
    path('api/goods-receive/create', GoodsReceiveNoteCreate.as_view(), name='goods-receive-note-create'),
    path('api/goods-receive/detail/<int:pk>', GoodsReceiveNoteDetail.as_view(), name='goods-receive-note-detail'),
    path('api/goods-receive/delete/<int:pk>', GoodsReceiveNoteDelete.as_view(), name='goods-receive-note-delete'),
    path('api/grn/confirm/<int:pk>', GoodsReceiveNoteConfirm.as_view(), name='goods-receive-note-confirm'),
    path('api/goods-receipt-notes/', GoodSReceiptNoteMasterSearchAPI.as_view(), name='goods-receipt-notes-search'),
    # For Supplier Payment
    path('api/supplier-payment/list', SupplierPaymentList.as_view(), name='supplier-payment-list'),
    path('api/supplier-payment/create', SupplierPaymenCreate.as_view(), name='supplier-payment-create'),
    path('api/supplier-payment/detail/<int:pk>', SupplierPaymenDetail.as_view(), name='supplier-payment-detail'),
    path('api/supplier-payment/delete/<int:pk>', SupplierPaymenDelete.as_view(), name='supplier-payment-delete'),
    path('api/sp/confirm/<int:pk>', SupplierPaymentConfirm.as_view(), name='supplier-payment-confirm'),


]