from django.urls import path
from .views import *

urlpatterns = [
    # For Notice Board Type
    path('api/notice-board', NoticeBoardCreateList.as_view(), name='notice-board-create-list'),
    path('api/notice-board/detail/<int:pk>', NoticeBoardDetails.as_view(), name='notice-board-retrive-update'),
    path('api/notice-board/delete/<int:pk>', NoticeBoardDelete.as_view(), name='notice-board-delete'),
    path('api/notice-board/file/<int:pk>', NoticeBoardFileUpload.as_view(), name='Notice-file-upload'),
    # For SMS Template
    path('api/sms-template/list', SmsTemplateList.as_view(), name='sms-template-list'),
    path('api/sms-template', SmsTemplateCreateList.as_view(), name='sms-template-create-list'),
    path('api/sms-template/detail/<int:pk>', SmsTemplateDetails.as_view(), name='sms-template-retrive-update'),
    path('api/sms-template/delete/<int:pk>', SmsTemplateDelete.as_view(), name='sms-template-delete'),
]