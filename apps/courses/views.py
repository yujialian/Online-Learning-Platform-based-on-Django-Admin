from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
# Create your views here.
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import View
from .models import Course, CourseResource, Video
from django.http import HttpResponse
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin

class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")

        hot_courses = Course.objects.all().order_by("-students")[:3]

        #course search
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))



        #course sort
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_num")

        # paging courses
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 9, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            "all_courses": courses,
            "sort": sort,
            "hot_courses":hot_courses
        })


class CourseDetailView(View):
    """
    Course detail page
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        #Add click nums
        course.click_num += 1
        course.save()
        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        tag = course.tags
        if tag:
            relate_courses = Course.objects.filter(Q(tags=tag) & ~Q(name=course.name))[:1]
        else:
            relate_courses = []


        return render(request, "course-detail.html", {
            "course":course,
            "relate_courses": relate_courses,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org
        })


class CourseInfoView(LoginRequiredMixin, View):
    """
    course chapter information
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        #check if user already this course
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            course.students += 1
            course.save()
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()


        user_courses = UserCourse.objects.filter(course=course)
        user_all_id = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_all_id)
        #get all course id
        course_all_id = [user_course.course.id for user_course in all_user_courses]
        #get other courses the user registered
        relate_courses = Course.objects.filter(id__in=course_all_id).order_by("-click_num")[:5]
        all_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-video.html", {
            "course":course,
            "all_resources": all_resources,
            "relate_courses": relate_courses
        })


class CourseCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()

        user_courses = UserCourse.objects.filter(course=course)
        user_all_id = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_all_id)
        # get all course id
        course_all_id = [user_course.course.id for user_course in all_user_courses]
        # get other courses the user registered
        relate_courses = Course.objects.filter(id__in=course_all_id).order_by("-click_num")[:5]
        return render(request, "course-comment.html", {
            "course":course,
            "all_resources": all_resources,
            "all_comments": all_comments,
            "relate_courses": relate_courses
        })


class AddCommentsView(View):
    """
     user add course comments
    """
    def post(self,request):
        if not request.user.is_authenticated():
            #if user did not login
            return HttpResponse('{"status":"fail", "msg":"Please login first!"}', content_type='application/json')

        course_id = request.POST.get("course_id", 0)
        comment = request.POST.get("comment", "")
        if course_id > 0 and comment != "":
            course_comment = CourseComments()
            course = Course.objects.get(id=int(course_id))
            #get and filter: get only get exactly one element, but filter return a query set
            course_comment.course = course
            course_comment.course_id = course_id
            course_comment.comments = comment
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse('{"status":"success", "msg":"You add an comment!"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"Invalid comment!"}', content_type='application/json')


class VideoPlayView(View):
    """
    Video play page
    """
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        # check if user already this course
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_all_id = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_all_id)
        # get all course id
        course_all_id = [user_course.course.id for user_course in all_user_courses]
        # get other courses the user registered
        relate_courses = Course.objects.filter(id__in=course_all_id).order_by("-click_num")[:5]
        all_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-play.html", {
            "course": course,
            "all_resources": all_resources,
            "relate_courses": relate_courses,
            "video":video
        })
