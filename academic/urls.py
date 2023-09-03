from django.urls import path,include
from .views import VersionList, VersionDetail, VersionDelete

urlpatterns = [
    path('api/version', VersionList.as_view(), name='version-list'),
    path('api/version/detail/<int:pk>', VersionDetail.as_view(), name='version-detail'),
    path('api/version/delete/<int:pk>', VersionDelete.as_view(), name='version-delete'),
]