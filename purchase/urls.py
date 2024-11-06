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

]