# _*_ coding: utf-8 _*_
__author__ = 'Yujia Lian'
__date__ = '7/4/17 1:22 AM'

from django.conf.urls import url, include
from .views import UserinfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView
from .views import MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseTView, MyMessageView

urlpatterns = [
    #User detail page
    url(r'^info/$', UserinfoView.as_view(), name="user_info"),

    #User head upload
    url(r'^image/upload/$', UploadImageView.as_view(), name= 'image_upload'),

    #user center change password
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update'),

    #send email verify code
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),

    # modify email
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),

    #My courses
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),

    # My course collection
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),

    # My teacher collection
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),

    # My course collection
    url(r'^myfav/course/$', MyFavCourseTView.as_view(), name='myfav_course'),

    # My message
    url(r'^mymessage/$', MyMessageView.as_view(), name='mymessage')
]