#_*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime
from organization.models import CourseOrg, Teacher
from django.db import models
from DjangoUeditor.models import UEditorField
# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name="Course organization", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"Course name")
    teacher = models.ForeignKey(Teacher, verbose_name="Professor", null=Teacher, blank=True)
    desc = models.CharField(max_length=300, verbose_name=u"Course description")
    category = models.CharField(default=u"back end",max_length=20, verbose_name=u"Course category")
    detail = UEditorField(verbose_name="Course detail",width=600, height=300, imagePath="courses/ueditor/", filePath="courses/ueditor/", default="")
    is_banner = models.BooleanField(default=False, verbose_name="add banner")
    degree = models.CharField(choices=(("cj", "Begining level"),("zj", "Middle level"), ("gj", "High level")),
                              max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name=u"Learning time(In minutes)")
    students = models.IntegerField(default=0, verbose_name=u"Total enrolled students")
    fav_nums = models.IntegerField(default=0, verbose_name=u"Favorite number")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"Cover", max_length=100)
    click_num = models.IntegerField(default=0, verbose_name=u"Click times")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"Add time")
    tags = models.CharField(default="", verbose_name="Course tag", max_length=100)
    you_need_know = models.CharField(default="", max_length=300, verbose_name="Course requirement")
    teacher_notice = models.CharField(default="", max_length=300, verbose_name="Teacher notice")

    class Meta:
        verbose_name = u"Course"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_chapter_nums(self):
        #get the chapter nums
        return self.lesson_set.all().count()

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        #get course all chapter
        return self.lesson_set.all()

    def get_relate_courses(self):

        return self.course_org.course_set[:5]


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"Course")
    name = models.CharField(max_length=100, verbose_name=u"Chapter name")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"Add time")

    class Meta:
        verbose_name = u"Chapter"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


    def get_lesson_video(self):
        #get chapter videos
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"Chapter")
    name = models.CharField(max_length=100, verbose_name=u"Video name")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"Add time")
    url = models.CharField(max_length=200, default="", verbose_name="url")
    learn_times = models.IntegerField(default=0, verbose_name=u"Learning time(In minutes)")


    class Meta:
        verbose_name = u"Course video"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"Course")
    name = models.CharField(max_length=100, verbose_name=u"name")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name=u"Resource files", max_length=100)
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"Add time")

    class Meta:
        verbose_name = u"Course resources"
        verbose_name_plural = verbose_name


class BannerCourse(Course):
    class Meta:
        verbose_name = "Banner course"
        verbose_name_plural = verbose_name
        proxy = True