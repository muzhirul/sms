from django.urls import path
from .views import *

urlpatterns = [
    path('api/bank', BankCreateList.as_view(), name='bank-list-create'),
]