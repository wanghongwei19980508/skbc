from django.conf.urls import url

from ..views.admin import CourseAnnouncementAPI, CourseAPI, CourseRoleAPI, LessonAPI, LessonAttachmentAPI, AttachmentAPI

urlpatterns = [
    url(r"^course/?$", CourseAPI.as_view(), name="course_admin_api"),
    url(r"^course/announcement/?$", CourseAnnouncementAPI.as_view(), name="course_announcement_admin_api"),
    url(r"^course/user/?$", CourseRoleAPI.as_view(), name="course_role_admin_api"),
    url(r"^course/lesson/?$", LessonAPI.as_view(), name="course_lesson_admin_api"),
    url(r"^lesson/attachment/?$", LessonAttachmentAPI.as_view(), name="lesson_attachment_admin_api"),
    url(r"^attachment/?$", AttachmentAPI.as_view(), name="attachment_admin_api"),
]