from django.urls import path
from .views import *

urlpatterns = [
    # For Warehouse
    path('api/warehouse/list', WareHouseList.as_view(), name='warehouse-list'),
    path('api/warehouse', WareHouseCreateList.as_view(), name='warehouse-create-list'),
    path('api/warehouse/detail/<int:pk>', WareHouseDetail.as_view(), name='warehouse-detail'),
    path('api/warehouse/delete/<int:pk>', WareHouseDelete.as_view(), name='warehouse-delete'),
    # For Brand
    path('api/brand/list', BrandeList.as_view(), name='brand-list'),
    path('api/brand', BrandCreateList.as_view(), name='brand-create-list'),
    path('api/brand/detail/<int:pk>', BrandDetail.as_view(), name='brand-detail'),
    path('api/brand/delete/<int:pk>', BrandDelete.as_view(), name='brand-delete'),

]