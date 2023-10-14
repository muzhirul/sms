from django.urls import path,include
from .views import GradeCreateList,GradeDetailUpdate,GradeDelete

urlpatterns = [
    path('api/grade', GradeCreateList.as_view(), name='grade-list-create'),
    path('api/grade/detail/<int:pk>', GradeDetailUpdate.as_view(), name='grade-detail-update'),
    path('api/grade/delete/<int:pk>', GradeDelete.as_view(), name='grade-delete'),
]