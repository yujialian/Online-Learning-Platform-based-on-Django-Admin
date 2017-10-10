#_*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u"Nick name", default="")
    birthday = models.DateField(verbose_name=u"Birthday", null=True, blank=True)
    gender = models.CharField(choices=(("male", "Gentleman"), ("female", "Lady")),default="female", max_length=10)
    address = models.CharField(max_length=100, default=u"")
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to="image/%Y/%m",default=u"image/default.png", max_length=100)

    class Meta:
        verbose_name = "Personal Information"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

    def unread_nums(self):
        #get unread message numbers
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"Verify code")
    email = models.EmailField(max_length=50, verbose_name=u"Email")
    send_type = models.CharField(choices=(("register", "Register"), ("Forget", u"Forget_password"), ("update_email", u"Update_email")), max_length=20)
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"Email verify code"
        verbose_name_plural = verbose_name#fushu

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"Title")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name=u"SlideWindow", max_length=100)#path of the image
    url = models.URLField(max_length=200, verbose_name=u"Visit address")
    index = models.IntegerField(default=100, verbose_name=u"Order")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"Add time")

    class Meta:
        verbose_name = u"Slide window"
        verbose_name_plural = verbose_name
