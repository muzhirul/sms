from django.urls import path,include
from .views import StudentList


urlpatterns = [
    path('api/student', StudentList.as_view(), name='student-list'),
]