from django.urls import path
from .views import *

urlpatterns = [
    # For Fees Type
    path('api/notice-board', NoticeBoardCreateList.as_view(), name='notice-board-create-list'),
]