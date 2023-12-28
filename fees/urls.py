from django.urls import path
from .views import *

urlpatterns = [
    # For Fees Type
    path('api/fees-type', FeesTypeCreateList.as_view(), name='fees-type-create-list'),
    path('api/fees-type/detail/<int:pk>', FeesTypeDetail.as_view(), name='fees-type-detail'),
    path('api/fees-type/delete/<int:pk>', FeesTypeDelete.as_view(), name='fees-type-delete'),
]