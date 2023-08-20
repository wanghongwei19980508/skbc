from django.db import models
from django.utils.timezone import now
from account.models import User
from utils.models import RichTextField
from utils.constants import CourseStatus, CourseType

class CourseTag(models.Model):
    name = models.TextField()

    class Meta:
        db_table = "course_tag"

# Create your models here.
class Course(models.Model):
    title = models.TextField()
    description = RichTextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    visible = models.BooleanField(default=True)
    password = models.TextField(null=True)
    pics = models.JSONField(null=True)
    is_template = models.BooleanField(default=False)
    tags = models.ManyToManyField(CourseTag)
    # 学生数量
    # enrolment = models.IntegerField(default=6)

    @property
    def status(self):
        if self.start_time > now():
            # 没有开始 返回1
            return CourseStatus.COURSE_NOT_START
        elif self.end_time < now():
            # 已经结束 返回-1
            return CourseStatus.COURSE_ENDED
        else:
            # 正在进行 返回0
            return CourseStatus.COURSE_UNDERWAY

    @property
    def course_type(self):
        if self.password:
            return CourseType.PASSWORD_PROTECTED_COURSE
        return CourseType.PUBLIC_COURSE

    class Meta:
        db_table = "course"
        ordering = ("-start_time",)

class CourseRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    # 0: student, 1: lecturer, 2: manager
    role = models.IntegerField(default=0)

    class Meta:
        db_table = "course_role"
        unique_together = ("user", "course", "role")

class CourseAnnouncement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.TextField()
    content = RichTextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    visible = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    top = models.BooleanField(default=False)

    class Meta:
        db_table = "course_announcement"
        ordering = ("-top","-create_time",)

class AttachmentTag(models.Model):
    name = models.TextField()

    class Meta:
        db_table = "attachment_tag"

class Attachment(models.Model):
    # display id
    _id = models.TextField(db_index=True)
    # 附件名
    name = models.TextField()
    # 附件描述
    description = models.TextField()
    # 是否可见
    visible = models.BooleanField(default=True)
    # 标签
    tags = models.ManyToManyField(AttachmentTag)
    # 上传时间
    upload_time = models.DateTimeField(auto_now_add=True)
    # 上传者
    upload_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # 附件路径或地址
    path = models.TextField()
    class Meta:
        db_table = "attachment"

class Lesson(models.Model):
    title = models.TextField()
    content = RichTextField()
    create_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    last_minutes = models.IntegerField(default=0)
    visible = models.BooleanField(default=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    ordinal = models.IntegerField(default=1)
    # 临时角色列表: 
    temporary_role = models.JSONField(null=True)

    class Meta:
        db_table = "lesson"
        ordering = ("ordinal",)
    
    @property
    def status(self):
        if self.start_time > now():
            # 没有开始 返回1
            return CourseStatus.COURSE_NOT_START
        elif self.end_time < now():
            # 已经结束 返回-1
            return CourseStatus.COURSE_ENDED
        else:
            # 正在进行 返回0
            return CourseStatus.COURSE_UNDERWAY

class LessonAttachment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    attachment = models.ForeignKey(Attachment, on_delete=models.CASCADE)
    class Meta:
        db_table = "lesson_attachment"
        unique_together = ("lesson", "attachment")