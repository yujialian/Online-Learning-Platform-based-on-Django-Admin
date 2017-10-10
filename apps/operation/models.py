# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from users.models import UserProfile
from courses.models import Course
# Create your models here.


class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"Name")
    mobile = models.CharField(max_length=11, verbose_name=u"Phone number")
    course_name = models.CharField(max_length=50, verbose_name=u"Course name")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"Add time")

    class Meta:
        verbose_name = u"User reference service"
        verbose_name_plural = verbose_name


class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"User")
    course = models.ForeignKey(Course, verbose_name=u"Course name")
    comments = models.CharField(max_length=200, verbose_name="Comments")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"Add time")

    class Meta:
        verbose_name = u"Course comments"
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"User")
    fav_id = models.IntegerField(default=0, verbose_name=u"Data ID")
    fav_type = models.IntegerField(choices=((1, "Courses"),(2, "Organization"), (3, "Teacher")), default=1, verbose_name=u"Favorite type")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"Add time")

    class Meta:
        verbose_name = u"User favorite"
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name=u"Receive user")
    message = models.CharField(max_length=200, verbose_name=u"Message content")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"Add time")
    has_read = models.BooleanField(default=False, verbose_name=u"Has read")

    class Meta:
        verbose_name = u"User Message"
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"Course name")
    user = models.ForeignKey(UserProfile,verbose_name="User name",default=None)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"Add time")

    class Meta:
        verbose_name = u"User course"
        verbose_name_plural = verbose_name
