from django.conf.urls import url

from ..views.oj import CourseAPI, CourseAnnouncementListAPI, CourseTagAPI, CourseRoleAPI, CoursesAsRole, LessonListAPI, LessonAPI, AttachmentTagAPI

urlpatterns = [
    url(r"^course/?$", CourseAPI.as_view(), name="course_api"),
    # url(r"^course/list/?$", CourseListAPI.as_view(), name="course_list_api"),
    url(r"^course/announcement/list/?$", CourseAnnouncementListAPI.as_view(), name="course_announcement_list_api"),
    url(r"^course/tags/?$", CourseTagAPI.as_view(), name="course_tag_list_api"),
    url(r"^course/user/?$", CourseRoleAPI.as_view(), name="course_role_api"),
    url(r"^course_as_role/list/?$", CoursesAsRole.as_view(), name="course_as_role_list_api"),
    url(r"^course/lesson/?$", LessonListAPI.as_view(), name="lesson_list_api"),
    url(r"^lesson/?$", LessonAPI.as_view(), name="lesson_detail_api"),
    url(r"^attachment/tags/?$", AttachmentTagAPI.as_view(), name="lesson_attachment_tag_list_api"),
]