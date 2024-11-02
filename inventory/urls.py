from django.urls import path
from .views import *

urlpatterns = [
    # For Warehouse
    path('api/warehouse/list', WareHouseList.as_view(), name='warehouse-list'),
    path('api/warehouse', WareHouseCreateList.as_view(), name='warehouse-create-list'),
    path('api/warehouse/detail/<int:pk>', WareHouseDetail.as_view(), name='warehouse-detail'),
    path('api/warehouse/delete/<int:pk>', WareHouseDelete.as_view(), name='warehouse-delete'),

]