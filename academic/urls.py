from django.urls import path,include
from .views import (VersionList, VersionDetail, VersionDelete,
                    SessionList, SessionDetail, SessionDelete,
                    SectionList,SectionDetail,SectionDelete,
                    SubjectList,SubjectDetail,SubjectDelete,
                    ClassList,ClassDetail,ClassDelete,
                    ClassRoomList,ClassRoomDetail)

urlpatterns = [
    # For version
    path('api/version', VersionList.as_view(), name='version-list'),
    path('api/version/detail/<int:pk>', VersionDetail.as_view(), name='version-detail'),
    path('api/version/delete/<int:pk>', VersionDelete.as_view(), name='version-delete'),
    # For Session
    path('api/session', SessionList.as_view(), name='session-list'),
    path('api/session/detail/<int:pk>', SessionDetail.as_view(), name='session-detail'),
    path('api/session/delete/<int:pk>', SessionDelete.as_view(), name='session-delete'),
    # For Section
    path('api/section', SectionList.as_view(), name='section-list'),
    path('api/section/detail/<int:pk>', SectionDetail.as_view(), name='section-detail'),
    path('api/section/delete/<int:pk>', SectionDelete.as_view(), name='section-delete'),
    # For Subject
    path('api/subject', SubjectList.as_view(), name='subject-list'),
    path('api/subject/detail/<int:pk>', SubjectDetail.as_view(), name='subject-detail'),
    path('api/subject/delete/<int:pk>', SubjectDelete.as_view(), name='subject-delete'),
    # For Class
    path('api/class', ClassList.as_view(), name='class-list'),
    path('api/class/detail/<int:pk>', ClassDetail.as_view(), name='class-detail'),
    path('api/class/delete/<int:pk>', ClassDelete.as_view(), name='class-delete'),
    # For Class Room
    path('api/class-room', ClassRoomList.as_view(), name='class-room-list'),
    path('api/class-room/detail/<int:pk>', ClassRoomDetail.as_view(), name='class-room-detail'),
]