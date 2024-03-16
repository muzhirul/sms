from django.urls import path,include
from .views import *

urlpatterns = [
    path('api/grade', GradeCreateList.as_view(), name='grade-list-create'),
    path('api/grade/detail/<int:pk>', GradeDetailUpdate.as_view(), name='grade-detail-update'),
    path('api/grade/delete/<int:pk>', GradeDelete.as_view(), name='grade-delete'),
    # For exam name
    path('api/exam-name', ExamNameCreateList.as_view(), name='exam-name-list-create'),
    # For Exam Routine 
    path('api/exam-routine/list', ExamRoutineList.as_view(), name='exam-routine-list'),
]