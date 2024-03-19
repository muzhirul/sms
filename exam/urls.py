from django.urls import path,include
from .views import *

urlpatterns = [
    path('api/grade', GradeCreateList.as_view(), name='grade-list-create'),
    path('api/grade/detail/<int:pk>', GradeDetailUpdate.as_view(), name='grade-detail-update'),
    path('api/grade/delete/<int:pk>', GradeDelete.as_view(), name='grade-delete'),
    # For exam name
    path('api/exam-name/list', ExamNameList.as_view(), name='exam-name-list'),
    path('api/exam-name', ExamNameCreateList.as_view(), name='exam-name-list-create'),
    path('api/exam-name/detail/<int:pk>', ExamNameDetailsList.as_view(), name='exam-name-detail-update'),
    path('api/exam-name/delete/<int:pk>', ExamNameDelete.as_view(), name='exam-name-delete'),
    # For Exam Routine 
    path('api/exam-routine', ExamRoutineCreateList.as_view(), name='exam-routine-create-list'),
]