# _*_ coding: utf-8 _*_
__author__ = 'Yujia Lian'
__date__ = '6/21/17 9:27 AM'
from django import forms
import re
from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """
        check if the phone number(US) is valid;
        """
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^(\\+?)\d{3,3}-?\d{2,2}-?\d{2,2}-?\d{3,3}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("The phone you enter must be valid!", code="mobile_invalid")
