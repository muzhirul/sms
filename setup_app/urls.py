from django.urls import path,include
from .views import ReligionList,BloodGroupList,GenderList,OccupationList

urlpatterns = [
    path('api/religion/list', ReligionList.as_view(), name='religion-list'),
    path('api/bloodgroup/list', BloodGroupList.as_view(), name='blood-group-list'),
    path('api/gender/list', GenderList.as_view(), name='gender-list'),
    path('api/occupation/list', OccupationList.as_view(), name='occupation-list'),
]