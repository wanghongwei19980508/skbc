from utils.api import APIView
from django.utils.timezone import now
from django.db.models import Q, Count
from ..models import Course, CourseStatus, CourseAnnouncement, CourseTag, CourseRole, Lesson, Attachment, AttachmentTag
from ..serializers import CourseSerializer, CourseAnnouncementSerializer, TagSerializer, CourseRoleSerializer, LessonOJSerializer, LessonSerializer, AttachmentTagSerializer
from account.decorators import login_required, check_course_permission, check_password
from utils.shortcuts import datetime2str, check_is_id

class CourseTagAPI(APIView):
    def get(self, request):
        qs = CourseTag.objects
        keyword = request.GET.get("keyword")
        if keyword:
            qs = CourseTag.objects.filter(name__icontains=keyword)
        tags = qs.annotate(course_count=Count("course")).filter(course_count__gt=0)
        return self.success(TagSerializer(tags, many=True).data)

class CourseAPI(APIView):
    def get(self, request):
        id = request.GET.get("course_id")
        user = request.user
        courseRole = CourseRole.objects.all().filter(user_id=request.user.id, course_id=id)
        if courseRole.count() == 0:
            return self.error("You are not in this course")
        if not id or not check_is_id(id):
            return self.error("Invalid parameter, id is required")
        try:
            contest = Course.objects.get(id=id, visible=True)
        except Course.DoesNotExist:
            return self.error("Course does not exist")
        data = CourseSerializer(contest).data
        data["now"] = datetime2str(now())
        return self.success(data)

class CourseListAPI(APIView):
    @login_required
    def get(self, request):
        courses = Course.objects.select_related("created_by").filter(is_template=False, visible=True)
        status = request.GET.get("status")
        # 搜索的情况
        keyword = request.GET.get("keyword", "").strip()
        if keyword:
            courses = courses.filter(Q(title__icontains=keyword) | Q(_id__icontains=keyword))
        # 按照标签筛选
        tag_text = request.GET.get("tag")
        if tag_text:
            courses = courses.filter(tags__name=tag_text)
        if status:
            cur = now()
            if status == CourseStatus.COURSE_NOT_START:
                courses = courses.filter(start_time__gt=cur)
            elif status == CourseStatus.COURSE_ENDED:
                courses = courses.filter(end_time__lt=cur)
            else:
                courses = courses.filter(start_time__lte=cur, end_time__gte=cur)
        return self.success(self.paginate_data(request, courses, CourseSerializer))

class AttachmentTagAPI(APIView):
    def get(self, request):
        qs = AttachmentTag.objects
        keyword = request.GET.get("keyword")
        if keyword:
            qs = AttachmentTag.objects.filter(name__icontains=keyword)
        tags = qs.annotate(attachment_count=Count("attachment")).filter(attachment_count__gt=0)
        return self.success(AttachmentTagSerializer(tags, many=True).data)

class LessonListAPI(APIView):
    @login_required
    @check_course_permission(check_type="lessons")
    def get(self, request):
        course_id = request.GET.get("course_id")
        if not course_id:
            return self.error("Invalid parameter, course_id is required")
        courseRoles = CourseRole.objects.all().filter(user_id=request.user.id, course_id=course_id)
        if courseRoles.count() == 0:
            return self.error("You are not in this course")
        lessonIds = Course.objects.all().filter(id=course_id).values('lesson')
        lessons = Lesson.objects.select_related("created_by").filter(id__in=lessonIds)
        return self.success(self.paginate_data(request, lessons, LessonOJSerializer))

class LessonAPI(APIView):
    @login_required
    @check_course_permission(check_type="lessons")
    def get(self, request):
        lesson_id = request.GET.get("lesson_id")
        if not lesson_id:
            return self.error("Invalid parameter, lesson_id is required")
        lesson = Lesson.objects.select_related("created_by").get(id=lesson_id)
        return self.success(LessonSerializer(lesson).data)

class CoursesAsRole(APIView):
    @login_required
    def get(self, request):
        course_role = request.GET.get("role")
        if course_role == "2" and request.user.can_mgmt_all_course():
            courses = Course.objects.select_related("created_by").filter(is_template=False, visible=True)
        else:
            roles = CourseRole.objects.all().filter(user_id=request.user.id, role=course_role)
            courses = Course.objects.select_related("created_by").filter(is_template=False, visible=True).filter(id__in=roles.values('course_id'))
        keyword = request.GET.get("keyword", "").strip()
        if keyword:
            courses = courses.filter(Q(title__icontains=keyword) | Q(created_by__username__icontains=keyword) | Q(tags__name__icontains=keyword))
        data = self.paginate_data(request, courses, CourseSerializer)
        return self.success(data)

class CourseAnnouncementListAPI(APIView):
    @check_course_permission(check_type="announcements")
    def get(self, request):
        course_id = request.GET.get("course_id")
        if not course_id:
            return self.error("Invalid parameter, course_id is required")
        data = CourseAnnouncement.objects.select_related("created_by").filter(course_id=course_id, visible=True)
        max_id = request.GET.get("max_id")
        if max_id:
            data = data.filter(id__gt=max_id)
        return self.success(CourseAnnouncementSerializer(data, many=True).data)
    
class CourseRoleAPI(APIView):
    @check_course_permission(check_type="role")
    def get(self, request):
        course_id = request.GET.get("course_id")
        if not course_id:
            return self.error("Invalid parameter, course_id is required")
        data = CourseRole.objects.select_related("user").filter(course_id=course_id)
        role = request.GET.get("role")
        if role:
            data = data.filter(role=role)
        return self.success(CourseRoleSerializer(data, many=True).data)