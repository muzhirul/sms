from django.urls import path,include
from .views import VersionList, VersionDetail

urlpatterns = [
    path('api/version', VersionList.as_view(), name='version-list'),
    path('api/version/detail/<int:pk>', VersionDetail.as_view(), name='version-detail'),
]