#_*_ encoding:utf-8 _*_
import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm
from .forms import UserInfoForm
from utils.email_send import send_register_email
from django.contrib.auth.hashers import make_password
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import Banner
from django.core.urlresolvers import reverse


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class RegisterView(View):

    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form':register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "User name you want to user already exist!"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            user_profile.save()

            #send welcome message
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "Welcome to Geek online education! Start learning today!"
            user_message.save()


            send_register_email(user_name, "register")
            return render(request, "send_success.html")
        else:
            return render(request, 'register.html', {'register_form': register_form})


class LogoutView(View):
    """
    logout
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):

    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)

                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html",
                                  {"msg": "User exist but does not active yet!"})
            else:
                return render(request, "login.html",
                              {"msg": "Username or password you entered is invalid, please try again!"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html",{"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)#passing a dict
        if forget_form.is_valid():
            email = request.POST.get("email", "")

            all_records = UserProfile.objects.all()
            all_email = []
            for record in all_records:
                all_email.append(record.email)
            if email in all_email:
                send_register_email(email, "forget")
                return render(request, "send_success.html")
            else:
                return render(request, "forgetpwd.html",
                              {"forget_form": forget_form, "msg": "The email you entered does not match!"})
        return render(request, "forgetpwd.html", {"forget_form": forget_form})


class ResetView(View):

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):

    """
    change user's password
    """

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "The password you entered does not match!"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            #Sending greeting information
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


class UserinfoView(LoginRequiredMixin, View):
    """
    user information
    """
    def get(self, request):
        return render(request, 'usercenter-info.html',{})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors),
                                content_type='application/json')



class UploadImageView(LoginRequiredMixin, View):
    """
    user change avatar
    """
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')



class UpdatePwdView(View):

    """
    change user's password in user center
    """

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"Passwords does not identical!"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors),
                                content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    send email verify code
    """
    def get(self, request):
        email = request.GET.get('email','')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"status":"fail"}','{"msg":"Email already been used."}', content_type='application/json')
        else:
            send_register_email(email, "update_email")
            return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        #change personal email
        email = request.POST.get('email','')
        code = request.POST.get('code','')
        existed_record = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_record:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"Verify code not match!"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """
    My courses page
    """
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            "user_courses": user_courses
        })


class MyFavOrgView(LoginRequiredMixin, View):
    """
    My favor collection page
    """

    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            "org_list": org_list
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    """
    My favor collection page
    """

    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            "teacher_list": teacher_list
        })


class MyFavCourseTView(LoginRequiredMixin, View):
    """
    My favor collection page
    """

    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            "course_list": course_list
        })


class MyMessageView(LoginRequiredMixin, View):
    """
    My message
    """
    def get(self, request):
        all_messsages = UserMessage.objects.filter(user=request.user.id)

        #mark unread messages as read when user check the message box
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # paging messages
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messsages, 5, request=request)
        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            "messages":messages
        })


class IndexView(View):
    #geek online main page
    def get(self, request):
        #get slide picture
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs
        })


def page_not_found(request):
    #404 page processing function
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    #404 page processing function
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response