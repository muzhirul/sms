from django.urls import path
from .views import *

urlpatterns = [
    # For Fees Type
    path('api/notice-board', NoticeBoardCreateList.as_view(), name='notice-board-create-list'),
    path('api/notice-board/detail/<int:pk>', NoticeBoardDetails.as_view(), name='notice-board-retrive-update'),
    path('api/notice-board/delete/<int:pk>', NoticeBoardDelete.as_view(), name='notice-board-delete'),
]