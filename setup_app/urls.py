from django.urls import path,include
from .views import *

urlpatterns = [
    path('api/religion/list', ReligionList.as_view(), name='religion-list'),
    path('api/bloodgroup/list', BloodGroupList.as_view(), name='blood-group-list'),
    path('api/gender/list', GenderList.as_view(), name='gender-list'),
    path('api/occupation/list', OccupationList.as_view(), name='occupation-list'),
    path('api/relation/list', RelationList.as_view(), name='relation-list'),
    path('api/day/list', DayList.as_view(), name='day-list'),
    path('api/floor/list', FloorList.as_view(), name='floor-list'),
    path('api/subject-type/list', SubjectTypeList.as_view(), name='subject-type-list'),
    # For Education Board
    path('api/board/list', EduBoardList.as_view(), name='education-board-list'),
    path('api/board', BoardCreateList.as_view(), name='Board-create-list'),
    path('api/board/detail/<int:pk>', BoardDetail.as_view(), name='board-detail'),
    path('api/board/delete/<int:pk>', BoardDelete.as_view(), name='board-delete'),
]