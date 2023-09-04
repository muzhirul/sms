from django.urls import path,include
from .views import VersionList, VersionDetail, VersionDelete,SessionList, SessionDetail, SessionDelete

urlpatterns = [
    # For version
    path('api/version', VersionList.as_view(), name='version-list'),
    path('api/version/detail/<int:pk>', VersionDetail.as_view(), name='version-detail'),
    path('api/version/delete/<int:pk>', VersionDelete.as_view(), name='version-delete'),
    # For Session
    path('api/session', SessionList.as_view(), name='session-list'),
    path('api/session/detail/<int:pk>', SessionDetail.as_view(), name='session-detail'),
    path('api/session/delete/<int:pk>', SessionDelete.as_view(), name='session-delete'),
]