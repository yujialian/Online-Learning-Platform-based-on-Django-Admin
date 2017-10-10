# _*_ coding: utf-8 _*_
__author__ = 'Yujia Lian'
__date__ = '6/6/17 1:52 AM'
import xadmin
from .models import EmailVerifyRecord, Banner, UserProfile
from xadmin import views
from xadmin.layout import Fieldset, Main, Side, Row
from xadmin.plugins.auth import UserAdmin

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class UserProfileAdmin(UserAdmin):
    pass


class GlobalSettings(object):
    site_title = "Geek education backend manage system"
    site_footer = "Geek education all rights reserved. Contact:yujia.lian001@gmail.com"
    menu_style = "accordion"

class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)