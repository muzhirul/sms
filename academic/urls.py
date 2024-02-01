from django.urls import path,include
from .views import *

urlpatterns = [
    # For version
    path('api/version/list', VersionViewList.as_view(), name='version-view-list'),
    path('api/version', VersionList.as_view(), name='version-list'),
    path('api/version/detail/<int:pk>', VersionDetail.as_view(), name='version-detail'),
    path('api/version/delete/<int:pk>', VersionDelete.as_view(), name='version-delete'),
    # For Session
    path('api/session/list', SessionViewList.as_view(), name='session-view-list'),
    path('api/session', SessionList.as_view(), name='session-list'),
    path('api/session/detail/<int:pk>', SessionDetail.as_view(), name='session-detail'),
    path('api/session/delete/<int:pk>', SessionDelete.as_view(), name='session-delete'),
    # For Section
    path('api/section/list', SectionViewList.as_view(), name='section-view-list'),
    path('api/section', SectionList.as_view(), name='section-list'),
    path('api/section/detail/<int:pk>', SectionDetail.as_view(), name='section-detail'),
    path('api/section/delete/<int:pk>', SectionDelete.as_view(), name='section-delete'),
    # For Subject
    path('api/subject/list', SubjectViewList.as_view(), name='subject-view-list'),
    path('api/subject', SubjectList.as_view(), name='subject-list'),
    path('api/subject/detail/<int:pk>', SubjectDetail.as_view(), name='subject-detail'),
    path('api/subject/delete/<int:pk>', SubjectDelete.as_view(), name='subject-delete'),
    # For Class
    path('api/class/list', ClassViewList.as_view(), name='class-view-list'),
    path('api/class', ClassList.as_view(), name='class-list'),
    path('api/class/detail/<int:pk>', ClassDetail.as_view(), name='class-detail'),
    path('api/class/delete/<int:pk>', ClassDelete.as_view(), name='class-delete'),
    # For Class Room
    path('api/class-room/list', ClassRoomViewList.as_view(), name='class-room-view-list'),
    path('api/class-room', ClassRoomList.as_view(), name='class-room-list'),
    path('api/class-room/detail/<int:pk>', ClassRoomDetail.as_view(), name='class-room-detail'),
    path('api/class-room/delete/<int:pk>', ClassRoomDelete.as_view(), name='class-room-delete'),
    # For Class Period
    path('api/class-period/list', ClassPeriodViewList.as_view(), name='class-period-view-list'),
    path('api/class-period', ClassPeriodList.as_view(), name='class-period-list'),
    path('api/class-period/detail/<int:pk>', ClassPeriodDetail.as_view(), name='class-period-detail'),
    path('api/class-period/delete/<int:pk>', ClassPeriodDelete.as_view(), name='class-period-delete'),
    # For Class section
    path('api/class-section/list', ClassSectionViewList.as_view(), name='class-section-view-list'),
    path('api/class-section', ClassSectionList.as_view(), name='class-section-list'),
    path('api/class-section/detail/<int:pk>', ClassSectionDetail.as_view(), name='class-section-detail'),
    path('api/class-section/delete/<int:pk>', ClassSectionDelete.as_view(), name='class-section-delete'),
    # For Class Subject
    path('api/class-subject/list', ClassSubjectViewList.as_view(), name='class-subject-view-list'),
    path('api/class-subject', ClassSubjectList.as_view(), name='class-subject-list'),
    path('api/class-subject/detail/<int:pk>', ClassSubjectDetail.as_view(), name='class-subject-detail'),
    path('api/class-subject/delete/<int:pk>', ClassSubjectDelete.as_view(), name='class-subject-delete'),
    # For Class Routine
    path('api/class-routine', ClassRoutineCreateList.as_view(), name='class-routine-list'),
    path('api/class-routine/detail/<int:pk>', ClassRoutineDetail.as_view(), name='class-routine-detail'),
    path('api/class-routine/delete/<int:pk>', ClassRoutineDelete.as_view(), name='class-routine-delete'),
    # For Group
    path('api/group/list', GroupViewCreate.as_view(), name='group-view-list'),
    path('api/group', GroupListCreate.as_view(), name='group-list'),
    path('api/group/detail/<int:pk>', GroupUpdateDetail.as_view(), name='group-detail'),
    path('api/group/delete/<int:pk>', GroupDelete.as_view(), name='group-delete'),
    # For Class teacher
    path('api/class-teacher', ClassTeacherCreateList.as_view(), name='class-teacher-list'),
    path('api/class-teacher/detail/<int:pk>', ClassTeacherDetail.as_view(), name='class-teacher-detail'),
    path('api/class-teacher/delete/<int:pk>', ClassTeacherDelete.as_view(), name='class-teacher-delete'),
    # For Class Routine v2
    path('api/class-routine/list', ClassRoutineList.as_view(), name='class-routine-list'),
    path('api/v2/class-routine', ClassRoutinev2CreateList.as_view(), name='class-routine-v2-list'),
    path('api/class-routine/v2/detail/<int:pk>', ClassRoutinev2Detail.as_view(), name='class-routine-v2-detail'),
    path('api/class-routine/v2/delete/<int:pk>', ClassRoutinev2Delete.as_view(), name='class-routine-v2-delete'),
    path('api/class-routine/detalis/delete/<int:pk>', ClassRoutineDetailsDelete.as_view(), name='class-routine-details-delete'),
    path('api/class-routine/search', ClassRoutineSearch.as_view(), name='class-routine-search'),
    # Teacher Time Table
    path('api/teacher-timetable/<str:staff_id>', TeacherTimeTableList.as_view(), name='teacher-timetable-list'),
]