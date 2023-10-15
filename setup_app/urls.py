from django.urls import path,include
from .views import ReligionList,BloodGroupList,GenderList,OccupationList,RelationList,DayList,FloorList

urlpatterns = [
    path('api/religion/list', ReligionList.as_view(), name='religion-list'),
    path('api/bloodgroup/list', BloodGroupList.as_view(), name='blood-group-list'),
    path('api/gender/list', GenderList.as_view(), name='gender-list'),
    path('api/occupation/list', OccupationList.as_view(), name='occupation-list'),
    path('api/relation/list', RelationList.as_view(), name='relation-list'),
    path('api/day/list', DayList.as_view(), name='day-list'),
    path('api/floor/list', FloorList.as_view(), name='floor-list'),
]