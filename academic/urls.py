from django.urls import path,include
from .views import VersionList

urlpatterns = [
    path('api/version', VersionList.as_view(), name='version-list'),
]