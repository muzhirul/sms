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
    # For Category
    path('api/category/list', CategoryList.as_view(), name='category-list'),
    path('api/category', CategoryCreateList.as_view(), name='category-create-list'),
    path('api/category/detail/<int:pk>', CategoryDetail.as_view(), name='category-detail'),
    path('api/category/delete/<int:pk>', CategoryDelete.as_view(), name='category-delete'),
    # For Model
    path('api/model/list', ModelList.as_view(), name='model-list'),
    path('api/model', ModelCreateList.as_view(), name='model-create-list'),
    path('api/model/detail/<int:pk>', ModelDetail.as_view(), name='model-detail'),
    path('api/model/delete/<int:pk>', ModelDelete.as_view(), name='model-delete'),
    # For Item 
    path('api/item/list', ItemList.as_view(), name='item-list'),
    path('api/item', ItemCreateList.as_view(), name='item-create-list'),
    path('api/item/detail/<int:pk>', ItemDetail.as_view(), name='item-detail'),
    path('api/item/delete/<int:pk>', ItemDelete.as_view(), name='item-delete'),
    # For Stock
    path('api/stock-masteer/list', StockMasterList.as_view(), name='stock-list'),

]