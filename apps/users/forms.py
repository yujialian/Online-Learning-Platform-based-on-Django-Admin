# _*_ coding: utf-8 _*_
__author__ = 'Yujia Lian'
__date__ = '6/11/17 1:18 PM'
from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile



class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):

    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": "The code you enter is invalid!"})


class ForgetForm(forms.Form):

    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": "The code you enter is invalid!"})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birthday', 'address', 'mobile']


