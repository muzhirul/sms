from django.urls import path
from .views import *

urlpatterns = [
    # For Fees Type
    path('api/fees-type', FeesCreateList.as_view(), name='fees-create-list'),
]