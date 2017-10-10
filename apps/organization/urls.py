# _*_ coding: utf-8 _*_
__author__ = 'Yujia Lian'
__date__ = '6/21/17 9:50 AM'

from django.conf.urls import url, include
from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView
from .views import AddFavView, TeacherListView, TeacherDetailView
urlpatterns = [
    #course organization list
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
    url(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),

    #collection
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),

    #Teacher list page
    url(r'^teacher/list/$', TeacherListView.as_view(), name="teacher_list"),

    #teacher detail page
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail")
]