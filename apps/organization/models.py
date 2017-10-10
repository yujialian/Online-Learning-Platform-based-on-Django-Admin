#_*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from django.db import models
from datetime import datetime

# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"City")
    desc = models.CharField(max_length=200, verbose_name=u"City description")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"City"
        verbose_name_plural = verbose_name


    def __unicode__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"Organization name")
    desc = models.TextField(verbose_name=u"Organization description")
    click_nums = models.IntegerField(default=0, verbose_name=u"Click times")
    tag = models.CharField(default="Start", max_length=10, verbose_name="organization tag")
    fav_nums = models.IntegerField(default=0, verbose_name=u"Favorite times")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name=u"Logo", max_length=100)
    address = models.CharField(max_length=150, verbose_name=u"Organization address")
    city = models.ForeignKey(CityDict, verbose_name=u"Location")
    add_time = models.DateTimeField(default=datetime.now)
    category = models.CharField(default="eftc", verbose_name="Provider category", max_length=20, choices=(("eftc","education-focused technology company"),("plp", "Personal learning platform"),("u", "Univerisity")))
    students = models.IntegerField(default=0, verbose_name="Number of students")
    courses = models.IntegerField(default=0, verbose_name="Number of courses")
    class Meta:
        verbose_name = u"Course provider"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_teacher_nums(self):
        #get the organization's teacher num
        return self.teacher_set.all().count()

    def get_course_nums(self):
        return self.course_set.all().count()

    def get_org_courses(self):
        all_org_courses = self.course_set.all()
        all_org_courses = all_org_courses.order_by("-students")
        return all_org_courses[:2]



class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name=u"Subsidiary organ")
    name = models.CharField(max_length=50, verbose_name=u"Teacher name")
    work_years = models.IntegerField(default=0, verbose_name=u"Work times")
    work_company = models.CharField(max_length=50, verbose_name=u"Work company")
    work_position = models.CharField(max_length=50, verbose_name=u"Work position")
    points = models.CharField(max_length=50, verbose_name=u"Teaching characteristics")
    click_nums = models.IntegerField(default=0, verbose_name=u"Click times")
    fav_nums = models.IntegerField(default=0, verbose_name=u"Favorite times")
    add_time = models.DateTimeField(default=datetime.now)
    image = models.ImageField(default='', upload_to="teacher/%Y/%m", verbose_name=u"head", max_length=100)

    class Meta:
        verbose_name = u"Teacher"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_course_nums(self):
        return self.course_set.all().count()