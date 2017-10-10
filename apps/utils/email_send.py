# _*_ coding: utf-8 _*_
__author__ = 'Yujia Lian'
__date__ = '6/15/17 1:45 PM'

from random import Random
from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM
from django.core.mail import send_mail


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    if send_type == 'update_email':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == 'register':
        email_title = "Geek online education register url"
        email_body = "Please click the link below to active your account: http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = "Geek online education reset password link"
        email_body = "Please click the link below to reset your password: http://127.0.0.1:8000/reset/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    elif send_type == 'update_email':
        email_title = "Geek online education update email link"
        email_body = "Here is you geek education reset email code: {0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])


def random_str(randomlength=8):
    str = ''
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str
