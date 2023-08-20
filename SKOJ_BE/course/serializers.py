from utils.api import UsernameSerializer, serializers

from .models import Course, CourseAnnouncement, CourseTag, Lesson, AttachmentTag, Attachment, LessonAttachment

class CourseRoleSerializer(serializers.Serializer):
    user = UsernameSerializer()
    role = serializers.CharField()

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseTag
        fields = "__all__"

class AttachmentTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttachmentTag
        fields = "__all__"

class CreateCourseSeriaizer(serializers.Serializer):
    title = serializers.CharField(max_length=128)
    description = serializers.CharField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    password = serializers.CharField(allow_blank=True, max_length=32)
    visible = serializers.BooleanField(default=True)
    is_template = serializers.BooleanField(default=False)
    tags = serializers.ListField(child=serializers.CharField(max_length=32), allow_empty=False)

class EditCourseSeriaizer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=128)
    description = serializers.CharField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    password = serializers.CharField(allow_blank=True, allow_null=True, max_length=32)
    visible = serializers.BooleanField()
    is_template = serializers.BooleanField()
    tags = serializers.ListField(child=serializers.CharField(max_length=32), allow_empty=False)

class CourseAdminSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()
    status = serializers.CharField()
    course_type = serializers.CharField()
    tags = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

class CourseSerializer(CourseAdminSerializer):
    class Meta:
        model = Course
        exclude = ("password", "visible")

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

class LessonOJSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=128)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    content = serializers.CharField()
    visible = serializers.BooleanField()
    ordinal = serializers.IntegerField()
    status = serializers.CharField()

class CreateLessonSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    title = serializers.CharField(max_length=128)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    content = serializers.CharField()
    visible = serializers.BooleanField()
    ordinal = serializers.IntegerField()

class EditLessonSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=128, required=False)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    content = serializers.CharField(required=False, allow_blank=True)
    visible = serializers.BooleanField(required=False)
    ordinal = serializers.IntegerField()

class CourseAnnouncementSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()

    class Meta:
        model = CourseAnnouncement
        fields = "__all__"

class CreateCourseAnnouncementSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    title = serializers.CharField(max_length=128)
    content = serializers.CharField()
    visible = serializers.BooleanField()

class EditCourseAnnouncementSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=128, required=False)
    content = serializers.CharField(required=False, allow_blank=True)
    visible = serializers.BooleanField(required=False)

class LessonAdminSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()
    status = serializers.CharField()

    class Meta:
        model = Lesson
        fields = "__all__"

class CreateAttachmentSerializer(serializers.Serializer):
    _id = serializers.CharField(max_length=32, allow_blank=True, allow_null=True)
    name = serializers.CharField(max_length=1024)
    description = serializers.CharField()
    visible = serializers.BooleanField(default=False)
    path = serializers.CharField(allow_null=True)
    tags = serializers.ListField(child=serializers.CharField(max_length=32), allow_empty=False)

class EditAttachmentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    _id = serializers.CharField(max_length=32, allow_blank=True, allow_null=True)
    name = serializers.CharField(max_length=1024)
    description = serializers.CharField()
    visible = serializers.BooleanField(allow_null=True)
    path = serializers.CharField(allow_null=True)
    tags = serializers.ListField(child=serializers.CharField(max_length=32), allow_empty=False)

class AttachmentAdminSerializer(serializers.ModelSerializer):
    upload_by = UsernameSerializer()
    tags = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)

    class Meta:
        model = Attachment
        fields = "__all__"

class LessonAttachmentSerializer(serializers.ModelSerializer):
    attachment = AttachmentAdminSerializer()
    lesson = LessonAdminSerializer()
    class Meta:
        model = LessonAttachment
        fields = "__all__"