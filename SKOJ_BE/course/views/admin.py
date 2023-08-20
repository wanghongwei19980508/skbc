from ..serializers import ( CreateCourseSeriaizer, CourseAdminSerializer,
                            CourseSerializer, EditCourseSeriaizer,
                            CreateCourseAnnouncementSerializer, 
                            CourseAnnouncementSerializer, EditCourseAnnouncementSerializer,LessonAdminSerializer,
                            CreateLessonSerializer, LessonSerializer, EditLessonSerializer,
                            CreateAttachmentSerializer, EditAttachmentSerializer, AttachmentAdminSerializer, LessonAttachmentSerializer)
from ..models import Course, CourseAnnouncement, CourseTag, CourseRole, Lesson, Attachment, AttachmentTag, LessonAttachment
from account.models import User
from account.decorators import check_course_permission, ensure_created_by
from utils.api import APIView, validate_serializer
import dateutil.parser

class CourseRoleAPI(APIView):
    @check_course_permission(check_type="manage_course")
    def post(self, request):
        """
        Add course role.
        """
        data = request.data
        course_id = data.get("course_id")
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return self.error("Course does not exist")
        try:
            user = User.objects.get(id=data["user_id"])
        except User.DoesNotExist:
            return self.error("User does not exist")
        CourseRole.objects.create(course=course, user=user, role=data["role"])
        return self.success()

    @check_course_permission(check_type="manage_course")
    def delete(self, request):
        """
        Delete course role.
        """
        data = request.data
        course_id = data.get("course_id")
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return self.error("Course does not exist")
        try:
            user = User.objects.get(id=data["user_id"])
        except User.DoesNotExist:
            return self.error("User does not exist")
        role = data.get("role")
        if role:
            CourseRole.objects.filter(course=course, user=user, role=role).delete()
        else:
            return self.error("Role is required")
        return self.success()

class CourseAPI(APIView):
    @validate_serializer(CreateCourseSeriaizer)
    def post(self, request):
        """
        Create one Course.
        """
        data = request.data
        data["start_time"] = dateutil.parser.parse(data["start_time"])
        data["end_time"] = dateutil.parser.parse(data["end_time"])
        data["created_by"] = request.user
        if data["end_time"] <= data["start_time"]:
            return self.error("Start time must occur earlier than end time")
        if data.get("password") and data["password"] == "":
            data["password"] = None
        tags = data.pop("tags")
        course = Course.objects.create(**data)
        for item in tags:
            try:
                tag = CourseTag.objects.get(name=item)
            except CourseTag.DoesNotExist:
                tag = CourseTag.objects.create(name=item)
            course.tags.add(tag)
        course.save()
        return self.success(CourseSerializer(course).data)

    @validate_serializer(EditCourseSeriaizer)
    def put(self, request):
        """
        update Course
        """
        data = request.data
        try:
            course = Course.objects.get(id=data.pop("id"))
            ensure_created_by(course, request.user)
        except Course.DoesNotExist:
            return self.error("Course does not exist")
        data["start_time"] = dateutil.parser.parse(data["start_time"])
        data["end_time"] = dateutil.parser.parse(data["end_time"])
        if data["end_time"] <= data["start_time"]:
            return self.error("Start time must occur earlier than end time")
        if not data["password"]:
            data["password"] = None
        tags = data.pop("tags")
        course.tags.clear()
        for item in tags:
            try:
                tag = CourseTag.objects.get(name=item)
            except CourseTag.DoesNotExist:
                tag = CourseTag.objects.create(name=item)
            course.tags.add(tag)
        for k, v in data.items():
            setattr(course, k, v)
        course.save()
        return self.success(CourseAdminSerializer(course).data)

    def get(self, request):
        """
        Get one Course or Course list.
        """
        course_id = request.GET.get("id")
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
                ensure_created_by(course, request.user)
                return self.success(CourseAdminSerializer(course).data)
            except Course.DoesNotExist:
                return self.error("Course does not exist")

        courses = Course.objects.all().order_by("-create_time")
        if not request.user.can_mgmt_all_course():
            courses = courses.filter(created_by=request.user)
        keyword = request.GET.get("keyword")
        if keyword:
            courses = courses.filter(title__contains=keyword)
        return self.success(self.paginate_data(request, courses, CourseAdminSerializer))

class CourseAnnouncementAPI(APIView):
    @validate_serializer(CreateCourseAnnouncementSerializer)
    def post(self, request):
        """
        Create one Course_announcement.
        """
        data = request.data
        try:
            course = Course.objects.get(id=data.pop("course_id"))
            ensure_created_by(course, request.user)
            data["course"] = course
            data["created_by"] = request.user
        except Course.DoesNotExist:
            return self.error("Course does not exist")
        announcement = CourseAnnouncement.objects.create(**data)
        return self.success(CourseAnnouncementSerializer(announcement).data)

    @validate_serializer(EditCourseAnnouncementSerializer)
    def put(self, request):
        """
        update Course_announcement
        """
        data = request.data
        try:
            course_announcement = CourseAnnouncement.objects.get(id=data.pop("id"))
            ensure_created_by(course_announcement, request.user)
        except CourseAnnouncement.DoesNotExist:
            return self.error("Course announcement does not exist")
        for k, v in data.items():
            setattr(course_announcement, k, v)
        course_announcement.save()
        return self.success()

    def delete(self, request):
        """
        Delete one Course_announcement.
        """
        course_announcement_id = request.GET.get("id")
        if course_announcement_id:
            if request.user.is_admin():
                CourseAnnouncement.objects.filter(id=course_announcement_id,
                                                   course__created_by=request.user).delete()
            else:
                CourseAnnouncement.objects.filter(id=course_announcement_id).delete()
        return self.success()

    def get(self, request):
        """
        Get one Course_announcement or Course_announcement list.
        """
        course_announcement_id = request.GET.get("id")
        if course_announcement_id:
            try:
                course_announcement = CourseAnnouncement.objects.get(id=course_announcement_id)
                ensure_created_by(course_announcement, request.user)
                return self.success(CourseAnnouncementSerializer(course_announcement).data)
            except CourseAnnouncement.DoesNotExist:
                return self.error("Course announcement does not exist")

        course_id = request.GET.get("course_id")
        if not course_id:
            return self.error("Parameter error")
        course_announcements = CourseAnnouncement.objects.filter(course_id=course_id)
        if request.user.is_admin():
            course_announcements = course_announcements.filter(created_by=request.user)
        keyword = request.GET.get("keyword")
        if keyword:
            course_announcements = course_announcements.filter(title__contains=keyword)
        return self.success(CourseAnnouncementSerializer(course_announcements, many=True).data)
    
class LessonAPI(APIView):
    @validate_serializer(CreateLessonSerializer)
    def post(self, request):
        """
        Create one Course_announcement.
        """
        data = request.data
        try:
            course = Course.objects.get(id=data.pop("course_id"))
            ensure_created_by(course, request.user)
            data["course"] = course
            data["created_by"] = request.user
        except Course.DoesNotExist:
            return self.error("Course does not exist")
        lesson = Lesson.objects.create(**data)
        return self.success(LessonSerializer(lesson).data)

    @validate_serializer(EditLessonSerializer)
    def put(self, request):
        """
        update Course_announcement
        """
        data = request.data
        try:
            lesson = Lesson.objects.get(id=data.pop("id"))
            ensure_created_by(lesson, request.user)
        except Lesson.DoesNotExist:
            return self.error("Course announcement does not exist")
        for k, v in data.items():
            setattr(lesson, k, v)
        lesson.save()
        return self.success()

    def delete(self, request):
        """
        Delete one lesson.
        """
        lesson_id = request.GET.get("id")
        if lesson_id:
            if request.user.is_admin():
                Lesson.objects.filter(id=lesson_id,
                                                   course__created_by=request.user).delete()
            else:
                Lesson.objects.filter(id=lesson_id).delete()
        return self.success()

    def get(self, request):
        """
        Get one Course_announcement or Course_announcement list.
        """
        lesson_id = request.GET.get("id")
        if lesson_id:
            try:
                lesson = Lesson.objects.get(id=lesson_id)
                ensure_created_by(lesson, request.user)
                return self.success(LessonAdminSerializer(lesson).data)
            except Lesson.DoesNotExist:
                return self.error("Course announcement does not exist")

        course_id = request.GET.get("course_id")
        if not course_id:
            return self.error("Parameter error")
        lessons = Lesson.objects.filter(course_id=course_id)
        if request.user.is_admin():
            lessons = lessons.filter(created_by=request.user)
        keyword = request.GET.get("keyword")
        if keyword:
            lessons = lessons.filter(title__contains=keyword)
        return self.success(self.paginate_data(request, lessons, LessonSerializer))
    
class AttachmentAPI(APIView):
    @validate_serializer(CreateAttachmentSerializer)
    def post(self, request):
        """
        Create one Attachment
        """
        data = request.data
        data["upload_by"] = request.user
        tags = data.pop("tags")
        attachment = Attachment.objects.create(**data)
        for item in tags:
            try:
                tag = AttachmentTag.objects.get(name=item)
            except AttachmentTag.DoesNotExist:
                tag = AttachmentTag.objects.create(name=item)
            attachment.tags.add(tag)
        attachment.save()
        return self.success(AttachmentAdminSerializer(attachment).data)

    @validate_serializer(EditAttachmentSerializer)
    def put(self, request):
        """
        update Attachment
        """
        data = request.data
        try:
            attachment = Attachment.objects.get(id=data.pop("id"))
        except Attachment.DoesNotExist:
            return self.error("Attachment does not exist")
        tags = data.pop("tags")
        attachment.tags.clear()
        for item in tags:
            try:
                tag = AttachmentTag.objects.get(name=item)
            except AttachmentTag.DoesNotExist:
                tag = AttachmentTag.objects.create(name=item)
            attachment.tags.add(tag)
        for k, v in data.items():
            setattr(attachment, k, v)
        attachment.save()
        return self.success()

    def delete(self, request):
        """
        Delete one Attachment.
        """
        attachment_id = request.GET.get("id")
        if attachment_id:
            if request.user.is_admin():
                Attachment.objects.filter(id=attachment_id, upload_by=request.user).delete()
            else:
                Attachment.objects.filter(id=attachment_id).delete()
        return self.success()

    def get(self, request):
        """
        Get one Attachment or Attachment list.
        """
        attachment_id = request.GET.get("id")
        if attachment_id:
            try:
                attachment = Attachment.objects.get(id=attachment_id)
                return self.success(AttachmentAdminSerializer(attachment).data)
            except Attachment.DoesNotExist:
                return self.error("Attachment does not exist")

        attachments = Attachment.objects.all()
        if request.user.is_admin():
            attachments = attachments.filter(upload_by=request.user)
        keyword = request.GET.get("keyword")
        if keyword:
            attachments = attachments.filter(name__contains=keyword)
        return self.success(self.paginate_data(request, attachments, AttachmentAdminSerializer))

class LessonAttachmentAPI(APIView):
    def post(self, request):
        """
        Create one Lesson Attachment
        """
        data = request.data
        lesson_id = data.pop("lesson_id")
        attachment_id = data.pop("attachment_id")
        try:
            lesson = Lesson.objects.get(id=lesson_id)
            attachment = Attachment.objects.get(id=attachment_id)
        except Lesson.DoesNotExist:
            return self.error("Lesson does not exist")
        except Attachment.DoesNotExist:
            return self.error("Attachment does not exist")
        
        LessonAttachment.objects.create(lesson=lesson, attachment=attachment)
        return self.success()

    def delete(self, request):
        """
        Delete one lesson attachment.
        """
        lesson_id = request.GET.get("lesson_id")
        attachment_id = request.GET.get("attachment_id")
        try:
            lesson = Lesson.objects.get(id=lesson_id)
            attachment = Attachment.objects.get(id=attachment_id)
        except Lesson.DoesNotExist:
            return self.error("Lesson does not exist")
        except Attachment.DoesNotExist:
            return self.error("Attachment does not exist")
        LessonAttachment.objects.filter(lesson=lesson, attachment=attachment).delete()
        return self.success()

    def get(self, request):
        """
        Get one Lesson Attachment or Lesson Attachment list.
        """
        lesson_id = request.GET.get("lesson_id")
        if lesson_id:
            try:
                lesson = Lesson.objects.get(id=lesson_id)
            except Lesson.DoesNotExist:
                return self.error("Lesson does not exist")
            attachments = LessonAttachment.objects.filter(lesson=lesson)
            return self.success(self.paginate_data(request, attachments, LessonAttachmentSerializer))

        attachment_id = request.GET.get("attachment_id")
        if attachment_id:
            try:
                attachment = Attachment.objects.get(id=attachment_id)
            except Attachment.DoesNotExist:
                return self.error("Attachment does not exist")
            lessons = LessonAttachment.objects.filter(attachment=attachment)
            return self.success(self.paginate_data(request, lessons, LessonAttachmentSerializer))
        
        return self.error("Parameter error")